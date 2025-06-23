import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from . import routes, models
from .utils import configure_logging, NotificationManager
from .fetchers import start_background_fetchers

# --- Logging ---
configure_logging()
logger = logging.getLogger("flashrisk.main")

# --- Environment Variables ---
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"

# --- FastAPI App ---
app = FastAPI(
    title="FlashRisk - Real-Time Disaster Alert System",
    description="AI-powered, real-time disaster detection & alerting platform. "
                "Provides APIs, live data, and robust notification infrastructure.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "A-P-U-R-B-O",
        "url": "https://github.com/A-P-U-R-B-O",
        "email": "your@email.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# --- Middleware: CORS, Compression, Metrics ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

if ENABLE_METRICS:
    app.add_middleware(PrometheusMiddleware, app_name="flashrisk")
    app.add_route("/metrics", handle_metrics)

# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {repr(exc)}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# --- Custom Root Redirect ---
@app.get("/", include_in_schema=False)
async def root():
    """Redirect to OpenAPI docs."""
    return RedirectResponse(url="/docs")

# --- Register API Routers ---
app.include_router(routes.router)

# --- Notification Manager ---
notification_manager = NotificationManager()

# --- Background Tasks ---
@app.on_event("startup")
async def on_startup():
    logger.info("Starting FlashRisk application...")
    await start_background_fetchers(app, notification_manager)
    logger.info("Background fetchers launched.")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down FlashRisk application.")

# --- OpenAPI Customization: Add Tags, Models, Branding ---
app.openapi_tags = [
    {"name": "System", "description": "Health checks & system endpoints."},
    {"name": "Disasters", "description": "Real-time disaster data APIs (earthquakes, weather, etc.)."},
    {"name": "Notifications", "description": "Test and manage alert notifications."},
]
app.openapi_schema = None  # Let FastAPI generate schema

# --- Advanced: Add Custom Middleware or Integrations Here ---
# (e.g., Sentry, SQL DB, advanced authentication)

logger.info("FlashRisk main application loaded.")
