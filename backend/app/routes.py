from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import asyncio
from dateutil.parser import parse as parse_date

router = APIRouter()

# In-memory storage for fetched events (demo only)
recent_earthquakes = []
recent_alerts = []

# Locks for concurrency safety
earthquake_lock = asyncio.Lock()
alert_lock = asyncio.Lock()

@router.get("/health", tags=["System"])
async def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/earthquakes", tags=["Disasters"])
async def get_earthquakes(limit: int = Query(10, ge=1, le=100)):
    """
    Get recent earthquake events.
    """
    async with earthquake_lock:
        # Return the most recent earthquakes up to limit
        return {"earthquakes": recent_earthquakes[:limit]}

@router.get("/alerts", tags=["Disasters"])
async def get_alerts(limit: int = Query(10, ge=1, le=100)):
    """
    Get recent weather or other disaster alerts.
    """
    async with alert_lock:
        # Return the most recent alerts up to limit
        return {"alerts": recent_alerts[:limit]}

@router.get("/notifications/test", tags=["Notifications"])
async def test_notification(channel: str = "email"):
    """
    Test notification endpoint (stub).
    """
    return JSONResponse({"detail": f"Test notification sent via {channel}"})

# Functions to update in-memory events (called from fetchers)

async def update_earthquakes(new_events: List[dict]):
    global recent_earthquakes
    async with earthquake_lock:
        # Merge new events first to prioritize freshness
        all_events = {e["id"]: e for e in new_events}
        for event in recent_earthquakes:
            if event["id"] not in all_events:
                all_events[event["id"]] = event

        # Optional: Sort by time descending (newest first)
        def get_event_time(e):
            try:
                return int(e.get("time", 0))
            except Exception:
                return 0

        events_list = list(all_events.values())
        events_list.sort(key=get_event_time, reverse=True)
        recent_earthquakes = events_list[:100]

async def update_alerts(new_alerts: List[dict]):
    global recent_alerts
    async with alert_lock:
        # Merge new alerts first to prioritize freshness
        all_alerts = {a["id"]: a for a in new_alerts}
        for alert in recent_alerts:
            if alert["id"] not in all_alerts:
                all_alerts[alert["id"]] = alert

        # Sort by date descending (newest first), handle missing or malformed dates gracefully
        def get_alert_date(a):
            date_str = a.get("date")
            if not date_str:
                return datetime.min
            try:
                return parse_date(date_str)
            except Exception:
                return datetime.min

        alerts_list = list(all_alerts.values())
        alerts_list.sort(key=get_alert_date, reverse=True)
        recent_alerts = alerts_list[:100]
