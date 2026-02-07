"""
Pydantic schemas for clothing and recommendation API operations.

Request schemas validate incoming data.
Response schemas control what gets serialized to JSON.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.constants.enums import (
    ClothingType,
    OccasionType,
    SeasonType,
    EventType,
    WeatherType,
    TimeOfDay,
)


class ClothingUploadRequest(BaseModel):
    """
    Manual metadata provided during clothing upload.
    Image is sent as a multipart file; these fields come as form data.
    """

    clothing_type: ClothingType
    occasion: OccasionType
    season: SeasonType


class ClothingResponse(BaseModel):
    """Response schema for a single clothing item."""

    id: int
    image_url: str
    dominant_color: Optional[str] = None
    secondary_color: Optional[str] = None
    clothing_type: str
    occasion: str
    season: str
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    """
    Input parameters for the outfit recommendation engine.
    All three fields are required to generate context-aware suggestions.
    """

    event: EventType
    weather: WeatherType
    time_of_day: TimeOfDay


class ScoredClothing(BaseModel):
    """A clothing item paired with its recommendation score and reasoning."""

    clothing: ClothingResponse
    score: int
    reasons: list[str]


class RecommendationResponse(BaseModel):
    """Response containing top outfit suggestions with explanations."""

    suggestions: list[ScoredClothing]
    event: str
    weather: str
    time_of_day: str
