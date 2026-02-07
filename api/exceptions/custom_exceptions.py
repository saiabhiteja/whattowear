"""
Custom domain exceptions for clean error handling.

Each exception maps to a specific business error,
making debugging and API responses more informative
than generic Exception messages.
"""


class ImageProcessingError(Exception):
    """Raised when image upload or processing fails."""

    def __init__(self, message: str = "Failed to process the uploaded image"):
        self.message = message
        super().__init__(self.message)


class InvalidClothingMetadataError(Exception):
    """Raised when clothing metadata is missing or invalid."""

    def __init__(
        self, message: str = "Invalid or incomplete clothing metadata"
    ):
        self.message = message
        super().__init__(self.message)


class RecommendationInputError(Exception):
    """Raised when recommendation request parameters are invalid."""

    def __init__(
        self, message: str = "Invalid recommendation input parameters"
    ):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    """Raised when user profile is not found in database."""

    def __init__(self, message: str = "User profile not found"):
        self.message = message
        super().__init__(self.message)


class CloudinaryUploadError(Exception):
    """Raised when Cloudinary image upload fails."""

    def __init__(
        self, message: str = "Failed to upload image to Cloudinary"
    ):
        self.message = message
        super().__init__(self.message)
