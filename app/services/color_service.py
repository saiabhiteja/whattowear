"""
Extracts and classifies dominant colors from clothing images.

Uses KMeans clustering to find the most prominent colors,
then maps RGB values to human-readable labels via
nearest-neighbor matching against reference colors.
"""
import logging
from typing import Optional

import cv2
import numpy as np
from sklearn.cluster import KMeans

from app.constants.color_constants import (
    COLOR_LABELS,
    KMEANS_CLUSTER_COUNT,
    MIN_CLUSTER_PERCENTAGE,
)
from app.exceptions.custom_exceptions import ImageProcessingError

logger = logging.getLogger(__name__)


def extract_dominant_colors(
    image: np.ndarray,
) -> tuple[np.ndarray, list[float]]:
    """
    Use KMeans clustering to find dominant colors in the image.

    Returns cluster centers (RGB) and their percentage of total pixels.
    KMeans is chosen because it's simple, deterministic with a fixed
    seed, and works well for color quantization tasks.
    """
    try:
        # Reshape image from (H, W, 3) to (N, 3) for KMeans input
        pixels = image.reshape(-1, 3)

        # Convert BGR to RGB since OpenCV loads images in BGR format
        pixels_rgb = cv2.cvtColor(
            pixels.reshape(1, -1, 3), cv2.COLOR_BGR2RGB
        ).reshape(-1, 3)

        kmeans = KMeans(
            n_clusters=KMEANS_CLUSTER_COUNT,
            random_state=42,
            n_init=10,
        )
        kmeans.fit(pixels_rgb)

        # Calculate what percentage of pixels belongs to each cluster
        _, counts = np.unique(kmeans.labels_, return_counts=True)
        total_pixels = len(kmeans.labels_)
        percentages = [count / total_pixels for count in counts]

        # Sort clusters by dominance (largest cluster first)
        sorted_indices = np.argsort(percentages)[::-1]
        sorted_centers = kmeans.cluster_centers_[sorted_indices]
        sorted_percentages = [percentages[i] for i in sorted_indices]

        return sorted_centers, sorted_percentages

    except Exception as exc:
        logger.error("Color extraction failed: %s", str(exc))
        raise ImageProcessingError(
            f"Failed to extract colors: {str(exc)}"
        ) from exc


def classify_color_label(rgb_values: np.ndarray) -> str:
    """
    Map an RGB color value to the nearest human-readable label.

    Uses Euclidean distance in RGB space - simple but effective
    for the distinct color categories we care about.
    More sophisticated methods (like CIEDE2000 in LAB space)
    are unnecessary for our coarse categories.
    """
    min_distance = float("inf")
    closest_label = "UNKNOWN"

    for label, reference_rgb in COLOR_LABELS.items():
        distance = np.sqrt(
            np.sum((rgb_values - np.array(reference_rgb)) ** 2)
        )
        if distance < min_distance:
            min_distance = distance
            closest_label = label

    return closest_label


def get_clothing_colors(
    image: np.ndarray,
) -> tuple[str, Optional[str]]:
    """
    Extract primary and optional secondary color labels from a clothing image.

    Secondary color is only reported if it represents a significant
    portion of the image (above MIN_CLUSTER_PERCENTAGE threshold).
    This filters out noise and small background patches.
    """
    centers, percentages = extract_dominant_colors(image)

    primary_color = classify_color_label(centers[0])
    logger.info(
        "Primary color detected: %s (%.1f%%)",
        primary_color,
        percentages[0] * 100,
    )

    secondary_color = None
    if len(centers) > 1 and percentages[1] >= MIN_CLUSTER_PERCENTAGE:
        secondary_color = classify_color_label(centers[1])
        logger.info(
            "Secondary color detected: %s (%.1f%%)",
            secondary_color,
            percentages[1] * 100,
        )

    return primary_color, secondary_color
