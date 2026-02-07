"""
API routes for outfit recommendations.

Accepts event context (event, weather, time of day),
runs the scoring engine against all wardrobe items,
and returns the top-scoring outfits with explanations.
"""
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.user import User
from api.models.clothing import Clothing
from api.constants.enums import SkinTone, SkinUndertone
from api.schemas.clothing_schema import (
    RecommendationRequest,
    RecommendationResponse,
    ScoredClothing,
    ClothingResponse,
)
from api.services.recommendation_service import get_top_recommendations
from api.exceptions.custom_exceptions import RecommendationInputError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendation", tags=["Recommendation"])


@router.post("/suggest", response_model=RecommendationResponse)
def suggest_outfit(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
):
    """
    Generate outfit suggestions based on event, weather, and time of day.

    Scores all clothing items against:
    - Event/occasion match
    - Weather-appropriate colors and seasons
    - Skin tone and undertone compatibility
    - Time-of-day color preferences

    Returns top 3 items sorted by score with reasoning.
    Works without a user profile, but recommendations are
    more personalized when skin analysis data is available.
    """
    try:
        # Fetch user skin profile (optional for recommendations)
        user = db.query(User).first()
        skin_tone = None
        skin_undertone = None

        if user and user.skin_tone:
            skin_tone = SkinTone(user.skin_tone)
        if user and user.skin_undertone:
            skin_undertone = SkinUndertone(user.skin_undertone)

        if not user or not user.skin_tone:
            logger.warning(
                "No skin profile found. "
                "Recommendations will be less personalized."
            )

        # Fetch all clothing items
        clothing_items = db.query(Clothing).all()
        if not clothing_items:
            raise RecommendationInputError(
                "No clothing items found. "
                "Please upload some clothes first."
            )

        # Score and rank clothing items
        top_items = get_top_recommendations(
            clothing_items=clothing_items,
            event=request.event,
            weather=request.weather,
            time_of_day=request.time_of_day,
            skin_tone=skin_tone,
            skin_undertone=skin_undertone,
        )

        # Build response with score explanations
        suggestions = [
            ScoredClothing(
                clothing=ClothingResponse.model_validate(item),
                score=score,
                reasons=reasons,
            )
            for item, score, reasons in top_items
        ]

        logger.info(
            "Recommendation generated: event=%s, weather=%s, results=%d",
            request.event.value,
            request.weather.value,
            len(suggestions),
        )

        return RecommendationResponse(
            suggestions=suggestions,
            event=request.event.value,
            weather=request.weather.value,
            time_of_day=request.time_of_day.value,
        )

    except RecommendationInputError as exc:
        raise HTTPException(
            status_code=400, detail=exc.message
        ) from exc
    except Exception as exc:
        logger.error("Recommendation error: %s", str(exc))
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while generating recommendations"
            ),
        ) from exc
