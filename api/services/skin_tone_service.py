"""
Analyzes user photos to determine skin tone and undertone.

Uses OpenCV Haar Cascade for face detection, then extracts
skin pixel colors in LAB color space for classification.
No deep learning is used - just color space analysis with thresholds.
"""
import logging

import cv2
import numpy as np

from api.constants.enums import SkinTone, SkinUndertone
from api.exceptions.custom_exceptions import ImageProcessingError

logger = logging.getLogger(__name__)

# Haar cascade XML ships with OpenCV - no extra download needed
HAAR_CASCADE_PATH = (
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ── LAB color space thresholds for skin tone classification ──────────
# L channel ranges from 0 (black) to 255 (white).
# These thresholds were chosen based on common skin tone research
# and can be tuned with real-world testing.
FAIR_SKIN_L_THRESHOLD = 170
DARK_SKIN_L_THRESHOLD = 120

# ── LAB 'b' channel thresholds for undertone classification ─────────
# Positive b values lean yellow/warm.
# Lower b values lean blue/cool.
WARM_B_THRESHOLD = 140
COOL_B_THRESHOLD = 125


def detect_face_region(image: np.ndarray) -> np.ndarray:
    """
    Detect the largest face in the image using Haar Cascade.
    Returns the cropped skin region (forehead-to-cheek area).

    Haar Cascade is chosen because it's lightweight, doesn't require
    a GPU, and is sufficient for single-face detection in clear photos.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
    )

    if len(faces) == 0:
        raise ImageProcessingError(
            "No face detected in the uploaded photo. "
            "Please upload a clear, front-facing photo."
        )

    # Use the largest detected face (most likely the actual face)
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face

    # Extract the forehead-to-cheek region (middle portion of face).
    # This avoids eyes, mouth, and hair which would skew color analysis.
    forehead_y = y + int(h * 0.15)
    cheek_y = y + int(h * 0.75)
    cheek_x_start = x + int(w * 0.2)
    cheek_x_end = x + int(w * 0.8)

    skin_region = image[forehead_y:cheek_y, cheek_x_start:cheek_x_end]
    logger.info("Face detected and skin region extracted")
    return skin_region


def extract_average_skin_color(skin_region: np.ndarray) -> np.ndarray:
    """
    Convert skin region to LAB color space and compute average values.

    LAB is used because:
    - L channel directly represents lightness (skin tone)
    - b channel correlates with warm/cool tones (undertone)
    This makes classification with simple thresholds reliable.
    """
    lab_image = cv2.cvtColor(skin_region, cv2.COLOR_BGR2LAB)
    average_lab = np.mean(lab_image.reshape(-1, 3), axis=0)
    logger.info(
        "Average LAB values: L=%.1f, A=%.1f, B=%.1f",
        average_lab[0],
        average_lab[1],
        average_lab[2],
    )
    return average_lab


def classify_skin_tone(lab_values: np.ndarray) -> SkinTone:
    """
    Determine skin tone category based on LAB L (lightness) channel.
    Higher L values indicate lighter skin.
    """
    lightness = lab_values[0]

    if lightness >= FAIR_SKIN_L_THRESHOLD:
        return SkinTone.FAIR
    elif lightness <= DARK_SKIN_L_THRESHOLD:
        return SkinTone.DARK
    else:
        return SkinTone.MEDIUM


def classify_skin_undertone(lab_values: np.ndarray) -> SkinUndertone:
    """
    Determine skin undertone based on LAB b channel.

    Positive b values lean yellow/warm, lower values lean blue/cool.
    This helps the recommendation engine suggest colors that
    complement the user's natural coloring.
    """
    b_channel = lab_values[2]

    if b_channel >= WARM_B_THRESHOLD:
        return SkinUndertone.WARM
    elif b_channel <= COOL_B_THRESHOLD:
        return SkinUndertone.COOL
    else:
        return SkinUndertone.NEUTRAL


def analyze_skin(
    image: np.ndarray,
) -> tuple[SkinTone, SkinUndertone]:
    """
    Full skin analysis pipeline:
    1. Detect face in the image
    2. Extract the skin-dominant region
    3. Classify tone (FAIR/MEDIUM/DARK) and undertone (WARM/COOL/NEUTRAL)
    """
    skin_region = detect_face_region(image)
    average_lab = extract_average_skin_color(skin_region)

    tone = classify_skin_tone(average_lab)
    undertone = classify_skin_undertone(average_lab)

    logger.info(
        "Skin analysis complete: tone=%s, undertone=%s",
        tone.value,
        undertone.value,
    )
    return tone, undertone
