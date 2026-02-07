"""
Score weights for the recommendation engine.

Extracted into constants so tuning the engine doesn't
require modifying business logic code. Each weight
represents how much influence a factor has on the
final outfit score.
"""

# Points awarded when the requested event matches clothing occasion.
# This is the strongest signal - wearing office clothes to office matters most.
EVENT_MATCH_SCORE = 3

# Points for weather-appropriate color choices.
# Light colors in heat, dark colors in cold.
WEATHER_COLOR_MATCH_SCORE = 2

# Points for skin-tone-appropriate colors.
# Certain colors visually complement specific skin tones.
SKIN_TONE_COLOR_MATCH_SCORE = 2

# Points for undertone-compatible colors.
# Warm/cool palettes harmonize with matching undertones.
UNDERTONE_COLOR_MATCH_SCORE = 2

# Points for time-of-day appropriate colors.
# Darker colors are more suitable for night events.
TIME_OF_DAY_MATCH_SCORE = 1

# Points for season-weather alignment.
# Summer clothing in hot weather, winter clothing in cold.
SEASON_WEATHER_MATCH_SCORE = 2

# Number of top recommendations to return from the engine.
TOP_RECOMMENDATIONS_COUNT = 3
