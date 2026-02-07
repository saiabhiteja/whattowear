"""
Entry point for Style Savvy API.

Initializes the FastAPI application, configures logging,
sets up the database, and registers all route modules.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings, setup_logging
from api.database import init_db
from api.routes import user_routes, clothing_routes, recommendation_routes

# Configure logging before anything else
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Application lifespan handler.
    Runs database initialization on startup.
    Using lifespan instead of deprecated on_event decorator.
    """
    init_db()
    logger.info("Application started successfully")
    yield
    logger.info("Application shutting down")


def create_app() -> FastAPI:
    """
    Application factory pattern.

    Creates and configures the FastAPI application instance.
    Using a factory allows easier testing and configuration
    without global side effects.
    """
    application = FastAPI(
        title=settings.app_name,
        description=(
            "A personal AI wardrobe recommendation system that analyzes "
            "skin tone and clothing colors to suggest outfits based on "
            "event, weather, and time of day."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # Enable CORS so the web app can call the API
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register route modules
    application.include_router(user_routes.router)
    application.include_router(clothing_routes.router)
    application.include_router(recommendation_routes.router)

    @application.get("/", tags=["Health"])
    def health_check():
        """Simple health check endpoint for uptime monitoring."""
        return {
            "status": "healthy",
            "app": settings.app_name,
        }

    return application


app = create_app()
