"""
Pydantic schemas for user-related API requests and responses.

Separating schemas from models keeps validation logic
independent of database concerns and makes the API
contract explicit.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from api.constants.enums import SkinTone, SkinUndertone


class UserProfileResponse(BaseModel):
    """Response schema for the GET /user/profile endpoint."""

    id: int
    photo_url: Optional[str] = None
    skin_tone: Optional[SkinTone] = None
    skin_undertone: Optional[SkinUndertone] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPhotoUploadResponse(BaseModel):
    """Response after successful photo upload and skin analysis."""

    message: str
    photo_url: str
    skin_tone: SkinTone
    skin_undertone: SkinUndertone
