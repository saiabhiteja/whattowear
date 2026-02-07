"""
SQLAlchemy model for clothing items.

Each row represents one piece of clothing in the user's wardrobe
with its color analysis results and manually-provided metadata.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from api.database import Base


class Clothing(Base):
    """
    Represents a clothing item in the user's wardrobe.

    dominant_color and secondary_color are extracted via KMeans analysis.
    clothing_type, occasion, and season are manual inputs for MVP
    (automatic classification would require deep learning).
    """

    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    dominant_color = Column(String, nullable=True)
    secondary_color = Column(String, nullable=True)
    clothing_type = Column(String, nullable=False)
    occasion = Column(String, nullable=False)
    season = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
