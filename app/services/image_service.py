"""
Handles image upload to Cloudinary and basic image preprocessing.

Cloudinary is used because Render's free tier has ephemeral storage -
uploaded files would be lost on every redeploy. Cloudinary's free tier
provides persistent image hosting with CDN delivery.
"""
import logging

import cloudinary
import cloudinary.uploader
import cv2
import numpy as np

from app.config import settings
from app.constants.color_constants import (
    CLOTHING_IMAGE_RESIZE_WIDTH,
    CLOTHING_IMAGE_RESIZE_HEIGHT,
)
from app.exceptions.custom_exceptions import (
    ImageProcessingError,
    CloudinaryUploadError,
)

logger = logging.getLogger(__name__)

# Configure Cloudinary credentials on module load
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)


def upload_image_to_cloudinary(image_bytes: bytes, folder: str) -> str:
    """
    Upload raw image bytes to Cloudinary and return the secure URL.

    Using a folder parameter to organize user photos vs clothing photos
    within the same Cloudinary account.
    """
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
