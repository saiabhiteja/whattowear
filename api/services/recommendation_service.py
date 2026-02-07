"""
Rule-based outfit recommendation engine.

Scores each clothing item against the user's context
(event, weather, time of day, skin tone/undertone)
and returns the top matches with explanations.

No ML models are used - this is intentionally simple,
interpretable, and easy to tune via score_weights.py.
"""
import logging
from typing import Optional

from api.constants.enums import (
    EventType,
    WeatherType,
    TimeOfDay,
    SkinTone,
    SkinUndertone,
)
from api.constants.color_constants import (
    WARM_PALETTE,
    COOL_PALETTE,
    NEUTRAL_PALETTE,
    LIGHT_COLORS,
    BRIGHT_COLORS,
    DARK_COLORS,
)
from api.constants.score_weights import (
    EVENT_MATCH_SCORE,
    WEATHER_COLOR_MATCH_SCORE,
    SKIN_TONE_COLOR_MATCH_SCORE,
    UNDERTONE_COLOR_MATCH_SCORE,
    TIME_OF_DAY_MATCH_SCORE,
    SEASON_WEATHER_MATCH_SCORE,
    TOP_RECOMMENDATIONS_COUNT,
)
from api.models.clothing import Clothing

logger = logging.getLogger(__name__)


def score_event_match(
    clothing: Clothing, event: EventType
) -> tuple[int, Optional[str]]:
    """
    Award points if the clothing's occasion matches the requested event.
    Direct match is the strongest signal for outfit appropriateness.
    """
    if clothing.occasion == event.value:
        return EVENT_MATCH_SCORE, f"Matches {event.value} occasion"
    return 0, None


def score_weather_color(
    clothing: Clothing, weather: WeatherType
) -> tuple[int, Optional[str]]:
    """
    Award points for weather-appropriate color choices.
    Light colors in hot weather improve comfort perception;
    dark colors in cold weather provide visual warmth.
    """
    color = clothing.dominant_color
    if color is None:
        return 0, None

    if weather == WeatherType.HOT and color in LIGHT_COLORS:
        return (
            WEATHER_COLOR_MATCH_SCORE,
            "Light color suitable for hot weather",
        )
    if weather == WeatherType.COLD and color in DARK_COLORS:
        return (
            WEATHER_COLOR_MATCH_SCORE,
            "Dark color suitable for cold weather",
        )
    return 0, None


def score_season_weather(
    clothing: Clothing, weather: WeatherType
) -> tuple[int, Optional[str]]:
    """
    Award points when clothing season aligns with weather.
    ALL-season items always get partial credit.
    """
    season = clothing.season

    if season == "ALL":
        return 1, "All-season clothing"
    if weather == WeatherType.HOT and season == "SUMMER":
        return (
            SEASON_WEATHER_MATCH_SCORE,
            "Summer clothing for hot weather",
        )
    if weather == WeatherType.COLD and season == "WINTER":
        return (
            SEASON_WEATHER_MATCH_SCORE,
            "Winter clothing for cold weather",
        )
    return 0, None


def score_skin_tone_compatibility(
    clothing: Clothing, skin_tone: Optional[SkinTone]
) -> tuple[int, Optional[str]]:
    """
    Award points for colors that complement the user's skin tone.
    Dark skin tones are enhanced by bright/vibrant colors;
    fair skin tones are complemented by deeper colors.
    """
    if skin_tone is None or clothing.dominant_color is None:
        return 0, None

    color = clothing.dominant_color

    if skin_tone == SkinTone.DARK and color in BRIGHT_COLORS:
        return (
            SKIN_TONE_COLOR_MATCH_SCORE,
            f"{color} complements dark skin tone",
        )
    if skin_tone == SkinTone.FAIR and color in DARK_COLORS:
        return (
            SKIN_TONE_COLOR_MATCH_SCORE,
            f"{color} complements fair skin tone",
        )
    return 0, None


def score_undertone_compatibility(
    clothing: Clothing, undertone: Optional[SkinUndertone]
) -> tuple[int, Optional[str]]:
    """
    Award points when clothing color belongs to the palette
    that harmonizes with the user's skin undertone.
    """
    if undertone is None or clothing.dominant_color is None:
        return 0, None

    color = clothing.dominant_color

    if undertone == SkinUndertone.WARM and color in WARM_PALETTE:
        return (
            UNDERTONE_COLOR_MATCH_SCORE,
            f"{color} harmonizes with warm undertone",
        )
    if undertone == SkinUndertone.COOL and color in COOL_PALETTE:
        return (
            UNDERTONE_COLOR_MATCH_SCORE,
            f"{color} harmonizes with cool undertone",
        )
    if undertone == SkinUndertone.NEUTRAL and color in NEUTRAL_PALETTE:
        return (
            UNDERTONE_COLOR_MATCH_SCORE,
            f"{color} works with neutral undertone",
        )
    return 0, None


def score_time_of_day(
    clothing: Clothing, time_of_day: TimeOfDay
) -> tuple[int, Optional[str]]:
    """
    Award points for time-appropriate color choices.
    Dark colors look more sophisticated at night events.
    """
    if clothing.dominant_color is None:
        return 0, None

    if (
        time_of_day == TimeOfDay.NIGHT
        and clothing.dominant_color in DARK_COLORS
    ):
        return (
            TIME_OF_DAY_MATCH_SCORE,
            "Dark color suitable for nighttime",
        )
    return 0, None


def score_clothing_item(
    clothing: Clothing,
    event: EventType,
    weather: WeatherType,
    time_of_day: TimeOfDay,
    skin_tone: Optional[SkinTone],
    skin_undertone: Optional[SkinUndertone],
) -> tuple[int, list[str]]:
    """
    Calculate total recommendation score for a single clothing item.

    Each scoring function is independent, making the system
    easy to extend with new rules without modifying existing ones.
    """
    total_score = 0
    reasons: list[str] = []

    scoring_results = [
        score_event_match(clothing, event),
        score_weather_color(clothing, weather),
        score_season_weather(clothing, weather),
        score_skin_tone_compatibility(clothing, skin_tone),
        score_undertone_compatibility(clothing, skin_undertone),
        score_time_of_day(clothing, time_of_day),
    ]

    for points, reason in scoring_results:
        total_score += points
        if reason is not None:
            reasons.append(reason)

    return total_score, reasons


def get_top_recommendations(
    clothing_items: list[Clothing],
    event: EventType,
    weather: WeatherType,
    time_of_day: TimeOfDay,
    skin_tone: Optional[SkinTone],
    skin_undertone: Optional[SkinUndertone],
) -> list[tuple[Clothing, int, list[str]]]:
    """
    Score all clothing items and return the top recommendations.

    Returns a list of (clothing, score, reasons) tuples
    sorted by score descending. Ties are broken by creation date.
    """
    scored_items = []

    for item in clothing_items:
        score, reasons = score_clothing_item(
            item, event, weather, time_of_day,
            skin_tone, skin_undertone,
        )
        scored_items.append((item, score, reasons))
        logger.info(
            "Scored item %d (%s): %d points",
            item.id,
            item.dominant_color,
            score,
        )

    # Sort by score descending
    scored_items.sort(key=lambda x: x[1], reverse=True)

    top_items = scored_items[:TOP_RECOMMENDATIONS_COUNT]
    logger.info(
        "Returning top %d recommendations out of %d items",
        len(top_items),
        len(clothing_items),
    )

    return top_items
