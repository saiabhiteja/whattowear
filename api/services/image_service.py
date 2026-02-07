"""
Handles image upload to Cloudinary or local storage.

When Cloudinary credentials are not set (e.g. local dev), images are
saved to the uploads/ directory and served by the API.
"""
import logging
import uuid
from pathlib import Path

import cv2
import numpy as np

from api.config import settings
from api.constants.color_constants import (
    CLOTHING_IMAGE_RESIZE_WIDTH,
    CLOTHING_IMAGE_RESIZE_HEIGHT,
)
from api.exceptions.custom_exceptions import (
    ImageProcessingError,
    CloudinaryUploadError,
)

logger = logging.getLogger(__name__)

# Only configure and use Cloudinary when credentials are set
def _is_cloudinary_configured() -> bool:
    return bool(
        settings.cloudinary_cloud_name
        and settings.cloudinary_api_key
        and settings.cloudinary_api_secret
    )


if _is_cloudinary_configured():
    import cloudinary
    import cloudinary.uploader

    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
    )


def _extension_for_bytes(image_bytes: bytes) -> str:
    """Return file extension based on image magic bytes."""
    if image_bytes[:2] == b"\xff\xd8":
        return ".jpg"
    if image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if image_bytes[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    return ".jpg"


def _upload_image_local(image_bytes: bytes, folder: str) -> str:
    """
    Save image to local uploads/ directory and return URL path.
    Used when Cloudinary is not configured (e.g. local development).
    """
    uploads_dir = Path("uploads") / folder
    uploads_dir.mkdir(parents=True, exist_ok=True)
    ext = _extension_for_bytes(image_bytes)
    name = f"{uuid.uuid4().hex}{ext}"
    path = uploads_dir / name
    path.write_bytes(image_bytes)
    url_path = f"/uploads/{folder}/{name}"
    logger.info("Image saved locally: %s", url_path)
    return url_path


def upload_image_to_cloudinary(image_bytes: bytes, folder: str) -> str:
    """
    Upload raw image bytes and return a URL (Cloudinary or local path).

    When Cloudinary is configured, uploads there. Otherwise saves to
    uploads/<folder>/ and returns a path like /uploads/<folder>/<id>.jpg
    that the API serves as static files.
    """
    if not _is_cloudinary_configured():
        return _upload_image_local(image_bytes, folder)

    try:
        result = cloudinary.uploader.upload(
            image_bytes,
            folder=f"wardrobe-ai/{folder}",
            resource_type="image",
        )
        image_url = result.get("secure_url")
        logger.info("Image uploaded to Cloudinary: folder=%s", folder)
        return image_url
    except Exception as exc:
        logger.error("Cloudinary upload failed: %s", str(exc))
        raise CloudinaryUploadError(
            f"Upload failed: {str(exc)}"
        ) from exc


def decode_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Convert raw image bytes into an OpenCV BGR image array.

    This avoids saving to disk, which is important for
    Render's ephemeral filesystem where files are lost on redeploy.
    """
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ImageProcessingError(
            "Could not decode the uploaded image. "
            "Please ensure it is a valid JPEG or PNG file."
        )

    return image


def resize_image_for_processing(image: np.ndarray) -> np.ndarray:
    """
    Resize image to a standard size for consistent and fast processing.

    Smaller images reduce KMeans clustering time significantly
    without meaningfully affecting color extraction accuracy.
    """
    resized = cv2.resize(
        image,
        (CLOTHING_IMAGE_RESIZE_WIDTH, CLOTHING_IMAGE_RESIZE_HEIGHT),
        interpolation=cv2.INTER_AREA,
    )
    return resized
