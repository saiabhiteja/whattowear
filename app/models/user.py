"""
SQLAlchemy model for user profile.

Stores skin analysis results that the recommendation engine
uses to suggest color-compatible outfits.
Single-user MVP - no authentication, just one profile row.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """
    Stores user photo analysis results.

    skin_tone and skin_undertone are populated after photo analysis
    and used by the recommendation engine to personalize suggestions.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(String, nullable=True)
    skin_tone = Column(String, nullable=True)
    skin_undertone = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
