"""
Color-related constants used across the application.

Centralizing these values makes tuning and debugging easier,
and prevents magic numbers scattered throughout the codebase.
"""

# Human-readable color labels mapped to their RGB reference values.
# Used by color_service to classify extracted colors via nearest-neighbor.
COLOR_LABELS: dict[str, tuple[int, int, int]] = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 128, 0),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 165, 0),
    "PINK": (255, 192, 203),
    "PURPLE": (128, 0, 128),
    "BROWN": (139, 69, 19),
    "GREY": (128, 128, 128),
    "BEIGE": (245, 245, 220),
    "NAVY": (0, 0, 128),
    "MAROON": (128, 0, 0),
    "OLIVE": (128, 128, 0),
    "TEAL": (0, 128, 128),
    "CREAM": (255, 253, 208),
    "LAVENDER": (230, 230, 250),
}

# Colors that pair well with warm skin undertones.
# Warm undertones are enhanced by earth tones and warm hues.
WARM_PALETTE: set[str] = {
    "RED", "ORANGE", "YELLOW", "BROWN", "BEIGE",
    "CREAM", "OLIVE", "MAROON",
}

# Colors that pair well with cool skin undertones.
# Cool undertones are enhanced by jewel tones and blue-based hues.
COOL_PALETTE: set[str] = {
    "BLUE", "NAVY", "PURPLE", "PINK", "LAVENDER",
    "TEAL", "GREY", "WHITE",
}

# Colors that work with neutral undertones (union of both palettes).
NEUTRAL_PALETTE: set[str] = WARM_PALETTE | COOL_PALETTE

# Light colors suitable for hot weather - improve comfort perception.
LIGHT_COLORS: set[str] = {
    "WHITE", "BEIGE", "CREAM", "PINK", "LAVENDER", "YELLOW",
}

# Bright/vibrant colors that complement darker skin tones.
BRIGHT_COLORS: set[str] = {
    "RED", "ORANGE", "YELLOW", "PINK", "PURPLE",
    "TEAL", "WHITE", "CREAM",
}

# Dark colors suitable for evening/night events.
DARK_COLORS: set[str] = {
    "BLACK", "NAVY", "MAROON", "BROWN",
}

# ── Image processing constants ──────────────────────────────────────
CLOTHING_IMAGE_RESIZE_WIDTH = 300
CLOTHING_IMAGE_RESIZE_HEIGHT = 300
KMEANS_CLUSTER_COUNT = 3

# Minimum percentage of pixels for a color to be considered secondary.
# Below this threshold, the cluster is likely noise or background.
MIN_CLUSTER_PERCENTAGE = 0.1
