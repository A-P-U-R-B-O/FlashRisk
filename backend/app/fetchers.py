import asyncio
import logging
import os
from datetime import datetime, timedelta

import httpx

from .utils import NotificationManager

logger = logging.getLogger("flashrisk.fetchers")

USGS_API = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson"
NOAA_API = "https://api.weather.gov/alerts/active"
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL_SECONDS", 60))  # seconds

async def fetch_usgs_earthquakes():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(USGS_API, timeout=10)
            response.raise_for_status()
            data = response.json()
            earthquakes = []
            for feature in data.get("features", []):
                props = feature["properties"]
                earthquake = {
                    "id": feature["id"],
                    "place": props["place"],
                    "mag": props["mag"],
                    "time": datetime.utcfromtimestamp(props["time"] / 1000),
                    "url": props["url"],
                }
                earthquakes.append(earthquake)
            return earthquakes
    except Exception as e:
        logger.error(f"USGS fetch error: {e}")
        return []

async def fetch_noaa_alerts():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NOAA_API, timeout=10)
            response.raise_for_status()
            data = response.json()
            alerts = []
            for feature in data.get("features", []):
                props = feature["properties"]
                alert = {
                    "id": feature["id"],
                    "event": props["event"],
                    "areaDesc": props.get("areaDesc", ""),
                    "severity": props.get("severity", ""),
                    "headline": props.get("headline", ""),
                    "description": props.get("description", ""),
                    "url": props.get("web", ""),
                    "sent": props.get("sent", ""),
                }
                alerts.append(alert)
            return alerts
    except Exception as e:
        logger.error(f"NOAA fetch error: {e}")
        return []

async def disaster_monitor_task(app, notification_manager: NotificationManager):
    """
    Main monitoring loop: fetches data, checks for new/critical events, and sends notifications.
    """
    logger.info("Disaster monitoring background task started.")
    seen_earthquakes = set()
    seen_alerts = set()

    while True:
        # USGS Earthquakes
        earthquakes = await fetch_usgs_earthquakes()
        for eq in earthquakes:
            if eq["id"] not in seen_earthquakes:
                seen_earthquakes.add(eq["id"])
                logger.info(f"New Earthquake: {eq}")
                await notification_manager.notify_all(
                    title=f"Earthquake Alert: {eq['place']} (M{eq['mag']})",
                    message=f"Time: {eq['time']}\nDetails: {eq['url']}"
                )

        # NOAA Alerts
        alerts = await fetch_noaa_alerts()
        for alert in alerts:
            if alert["id"] not in seen_alerts:
                seen_alerts.add(alert["id"])
                logger.info(f"New NOAA Alert: {alert}")
                await notification_manager.notify_all(
                    title=f"Weather Alert: {alert['event']} ({alert['severity']})",
                    message=f"{alert['headline']}\n{alert['description']}\nDetails: {alert['url']}"
                )

        await asyncio.sleep(FETCH_INTERVAL)

async def start_background_fetchers(app, notification_manager: NotificationManager):
    """
    Starts all background fetchers as asyncio tasks.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(disaster_monitor_task(app, notification_manager))
    logger.info("Background fetchers started.")
