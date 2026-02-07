"""
API routes for user profile and photo upload.

Handles face photo upload, skin analysis, and profile retrieval.
Single-user MVP - no authentication required.
"""
import logging

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.user import User
from api.schemas.user_schema import (
    UserProfileResponse,
    UserPhotoUploadResponse,
)
from api.services.image_service import (
    upload_image_to_cloudinary,
    decode_image_from_bytes,
)
from api.services.skin_tone_service import analyze_skin
from api.exceptions.custom_exceptions import (
    ImageProcessingError,
    CloudinaryUploadError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/upload-photo",
    response_model=UserPhotoUploadResponse,
)
async def upload_user_photo(
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a user's face photo for skin tone analysis.

    Process:
    1. Upload image to Cloudinary for persistent storage
    2. Detect face and extract skin region
    3. Classify skin tone and undertone
    4. Create or update user profile in database
    """
    try:
        image_bytes = await photo.read()

        # Upload to Cloudinary for persistent storage
        photo_url = upload_image_to_cloudinary(
            image_bytes, folder="user-photos"
        )

        # Decode and analyze skin tone/undertone
        image = decode_image_from_bytes(image_bytes)
        skin_tone, skin_undertone = analyze_skin(image)

        # Upsert user profile (single-user MVP: only one row)
        user = db.query(User).first()
        if user is None:
            user = User(
                photo_url=photo_url,
                skin_tone=skin_tone.value,
                skin_undertone=skin_undertone.value,
            )
            db.add(user)
        else:
            user.photo_url = photo_url
            user.skin_tone = skin_tone.value
            user.skin_undertone = skin_undertone.value

        db.commit()
        db.refresh(user)

        logger.info(
            "User photo processed: tone=%s, undertone=%s",
            skin_tone.value,
            skin_undertone.value,
        )

        return UserPhotoUploadResponse(
            message="Photo analyzed successfully",
            photo_url=photo_url,
            skin_tone=skin_tone,
            skin_undertone=skin_undertone,
        )

    except ImageProcessingError as exc:
        raise HTTPException(
            status_code=422, detail=exc.message
        ) from exc
    except CloudinaryUploadError as exc:
        raise HTTPException(
            status_code=502, detail=exc.message
        ) from exc
    except Exception as exc:
        logger.error(
            "Unexpected error during photo upload: %s", str(exc)
        )
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while processing your photo"
            ),
        ) from exc


@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(db: Session = Depends(get_db)):
    """
    Retrieve the current user's profile including skin analysis results.
    Returns 404 if no photo has been uploaded yet.
    """
    user = db.query(User).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="No user profile found. Please upload a photo first.",
        )
    return user
