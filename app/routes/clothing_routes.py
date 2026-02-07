"""
API routes for clothing item management.

Handles clothing image upload with color analysis
and retrieval of all wardrobe items.
"""
import logging

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.clothing import Clothing
from app.schemas.clothing_schema import ClothingResponse
from app.constants.enums import ClothingType, OccasionType, SeasonType
from app.services.image_service import (
    upload_image_to_cloudinary,
    decode_image_from_bytes,
    resize_image_for_processing,
)
from app.services.color_service import get_clothing_colors
from app.exceptions.custom_exceptions import (
    ImageProcessingError,
    CloudinaryUploadError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clothing", tags=["Clothing"])


@router.post("/upload", response_model=ClothingResponse)
async def upload_clothing(
    image: UploadFile = File(...),
    clothing_type: ClothingType = Form(...),
    occasion: OccasionType = Form(...),
    season: SeasonType = Form(...),
    db: Session = Depends(get_db),
):
    """
    Upload a clothing image with metadata.

    Process:
    1. Upload image to Cloudinary for persistent storage
    2. Decode and resize for efficient processing
    3. Extract dominant colors via KMeans clustering
    4. Store clothing record with colors and metadata

    clothing_type, occasion, and season are manual inputs for MVP
    because automatic classification would require deep learning.
    """
    try:
        image_bytes = await image.read()

        # Upload to Cloudinary for persistent storage
        image_url = upload_image_to_cloudinary(
            image_bytes, folder="clothing"
        )

        # Decode, resize, and extract colors
        cv_image = decode_image_from_bytes(image_bytes)
        resized = resize_image_for_processing(cv_image)
        primary_color, secondary_color = get_clothing_colors(resized)

        # Create clothing record in database
        clothing_item = Clothing(
            image_url=image_url,
            dominant_color=primary_color,
            secondary_color=secondary_color,
            clothing_type=clothing_type.value,
            occasion=occasion.value,
            season=season.value,
        )
        db.add(clothing_item)
        db.commit()
        db.refresh(clothing_item)

        logger.info(
            "Clothing uploaded: type=%s, color=%s",
            clothing_type.value,
            primary_color,
        )

        return clothing_item

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
            "Unexpected error during clothing upload: %s", str(exc)
        )
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while processing the clothing image"
            ),
        ) from exc


@router.get("/all", response_model=list[ClothingResponse])
def get_all_clothing(db: Session = Depends(get_db)):
    """Retrieve all clothing items in the wardrobe."""
    items = db.query(Clothing).all()
    return items
