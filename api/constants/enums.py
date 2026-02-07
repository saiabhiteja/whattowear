"""
Enums for all domain-specific categorical values.

Using enums instead of raw strings prevents typos,
enables IDE autocompletion, and makes the codebase
self-documenting. All enums inherit from str so they
serialize cleanly in JSON responses.
"""
from enum import Enum


class SkinTone(str, Enum):
    """Broad skin tone classification based on LAB luminance."""
    FAIR = "FAIR"
    MEDIUM = "MEDIUM"
    DARK = "DARK"


class SkinUndertone(str, Enum):
    """
    Skin undertone affects which clothing colors
    look harmonious on the wearer.
    """
    WARM = "WARM"
    COOL = "COOL"
    NEUTRAL = "NEUTRAL"


class ClothingType(str, Enum):
    """Supported clothing categories for MVP."""
    SHIRT = "SHIRT"
    TSHIRT = "TSHIRT"
    JEANS = "JEANS"
    TROUSERS = "TROUSERS"
    KURTA = "KURTA"
    JACKET = "JACKET"
    SHORTS = "SHORTS"
    DRESS = "DRESS"
    BLAZER = "BLAZER"
    HOODIE = "HOODIE"


class OccasionType(str, Enum):
    """Event/occasion categories for outfit matching."""
    CASUAL = "CASUAL"
    OFFICE = "OFFICE"
    PARTY = "PARTY"
    WEDDING = "WEDDING"
    TRADITIONAL = "TRADITIONAL"


class SeasonType(str, Enum):
    """Season suitability for clothing items."""
    SUMMER = "SUMMER"
    WINTER = "WINTER"
    ALL = "ALL"


class EventType(str, Enum):
    """Event type for recommendation API requests."""
    OFFICE = "OFFICE"
    CASUAL = "CASUAL"
    PARTY = "PARTY"
    WEDDING = "WEDDING"


class WeatherType(str, Enum):
    """Current weather condition for recommendation context."""
    HOT = "HOT"
    COLD = "COLD"
    RAINY = "RAINY"


class TimeOfDay(str, Enum):
    """Time of day affects color preference in recommendations."""
    DAY = "DAY"
    NIGHT = "NIGHT"
