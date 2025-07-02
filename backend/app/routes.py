from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime

router = APIRouter()

In-memory storage for fetched events (for demo; replace with DB/cache in production)

recent_earthquakes = []
recent_alerts = []

@router.get("/health", tags=["System"])
async def health_check():
"""
Basic health check endpoint.
"""
return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/earthquakes", tags=["Disasters"])
async def get_earthquakes(limit: Optional[int] = 10):
"""
Get recent earthquake events.
"""
# Return the most recent earthquakes up to limit
return {"earthquakes": recent_earthquakes[:limit]}

@router.get("/alerts", tags=["Disasters"])
async def get_alerts(limit: Optional[int] = 10):
"""
Get recent weather or other disaster alerts.
"""
# Return the most recent alerts up to limit
return {"alerts": recent_alerts[:limit]}

@router.get("/notifications/test", tags=["Notifications"])
async def test_notification(channel: str = "email"):
"""
Test notification endpoint (stub).
"""
# In production, trigger a real notification via NotificationManager
return JSONResponse({"detail": f"Test notification sent via {channel}"})

Functions to update in-memory events (called from fetchers)

def update_earthquakes(new_events: List[dict]):
global recent_earthquakes
# Prepend new events, keep unique, truncate to 100
all_events = {e["id"]: e for e in recent_earthquakes}
for event in new_events:
all_events[event["id"]] = event
recent_earthquakes = list(all_events.values())[:100]

def update_alerts(new_alerts: List[dict]):
global recent_alerts
# Prepend new alerts, keep unique, truncate to 100
all_alerts = {a["id"]: a for a in recent_alerts}
for alert in new_alerts:
all_alerts[alert["id"]] = alert
recent_alerts = list(all_alerts.values())[:100]
