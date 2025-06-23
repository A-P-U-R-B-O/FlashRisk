import logging
import os

from fastapi import FastAPI
from . import routes
from .fetchers import start_background_fetchers
from .utils import NotificationManager, configure_logging

# Configure logging
configure_logging()

logger = logging.getLogger("flashrisk")

# Load environment variables (example: from .env if using dotenv)
MODEL_PATH = os.getenv("MODEL_PATH", "./model")
ALERT_API_KEY = os.getenv("ALERT_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Initialize FastAPI app
app = FastAPI(
    title="FlashRisk - Real-Time Disaster Alert System",
    description="API and background services for real-time disaster detection, alerting, and dashboard integration.",
    version="1.0.0"
)

# Include API routes
app.include_router(routes.router)

# Initialize Notification Manager
notification_manager = NotificationManager(
    twilio_sid=TWILIO_ACCOUNT_SID,
    twilio_token=TWILIO_AUTH_TOKEN
)

# Start background fetchers for real-time monitoring
@app.on_event("startup")
async def startup_event():
    logger.info("Starting FlashRisk background fetchers...")
    await start_background_fetchers(app, notification_manager)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FlashRisk services...")
    # Add any cleanup logic if needed (e.g., close DB connections)

# Expose app for ASGI servers
__all__ = ["app", "notification_manager"]
