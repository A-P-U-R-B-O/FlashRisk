import asyncio
import httpx
import logging
from .routes import update_earthquakes, update_alerts

logger = logging.getLogger("flashrisk.fetchers")

USGS_API = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

# Main function FastAPI will call
async def start_background_fetchers(app, notification_manager):
    asyncio.create_task(fetch_and_update_earthquakes())
    logger.info("✔️ Earthquake background fetcher started")

async def fetch_and_update_earthquakes():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(USGS_API, timeout=10)
                res.raise_for_status()
                data = res.json()

                # Extract simplified event info
                events = [
                    {
                        "id": f["id"],
                        "mag": f["properties"]["mag"],
                        "place": f["properties"]["place"],
                        "time": f["properties"]["time"],
                        "url": f["properties"]["url"]
                    }
                    for f in data.get("features", [])
                ]

                update_earthquakes(events)
                logger.info(f"✅ Fetched and updated {len(events)} earthquakes.")
        except Exception as e:
            logger.warning(f"⚠️ Error fetching earthquakes: {e}")

        await asyncio.sleep(600)  # Repeat every 10 minutes
