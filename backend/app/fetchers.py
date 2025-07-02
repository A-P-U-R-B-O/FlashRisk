import asyncio
import httpx
import logging
from .routes import update_earthquakes, update_alerts

logger = logging.getLogger("flashrisk.fetchers")

USGS_API = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
RELIEFWEB_API = "https://api.reliefweb.int/v1/disasters?appname=FlashRisk&limit=20&sort[]=date:desc"

async def start_background_fetchers(app, notification_manager):
    asyncio.create_task(fetch_and_update_earthquakes())
    asyncio.create_task(fetch_and_update_alerts())
    logger.info("✔️ Earthquake and Alert background fetchers started")

async def fetch_and_update_earthquakes():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(USGS_API, timeout=10)
                res.raise_for_status()
                data = res.json()

                events = []
                for f in data.get("features", []):
                    props = f.get("properties", {})
                    # Only include earthquakes with required fields
                    if not (f.get("id") and props.get("mag") is not None and props.get("place") and props.get("time") and props.get("url")):
                        logger.warning(f"Skipping incomplete earthquake event: {f.get('id')}")
                        continue
                    event = {
                        "id": f["id"],
                        "mag": props["mag"],
                        "place": props["place"],
                        "time": props["time"],
                        "url": props["url"]
                    }
                    events.append(event)

                update_earthquakes(events)
                logger.info(f"✅ Fetched and updated {len(events)} earthquakes.")
        except Exception as e:
            logger.warning(f"⚠️ Error fetching earthquakes: {e}")

        await asyncio.sleep(600)  # 10 mins

async def fetch_and_update_alerts():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(RELIEFWEB_API, timeout=10)
                res.raise_for_status()
                data = res.json()

                alerts = []
                for d in data.get("data", []):
                    fields = d.get("fields", {})

                    # Use the "name" field and try to parse country and event type if possible
                    name = fields.get("name")
                    if not name:
                        logger.warning(f"Skipping alert with missing name (id={d.get('id')})")
                        continue

                    # Try to parse country and event type from the name (e.g. "Panama: River Pollution - Jun 2025")
                    if ":" in name:
                        country, rest = name.split(":", 1)
                        country = country.strip()
                        event_type = rest.split("-")[0].strip() if "-" in rest else rest.strip()
                    else:
                        country = None
                        event_type = name

                    alert = {
                        "id": str(d["id"]),
                        "type": event_type,
                        "country": country,
                        "name": name,
                        "url": d.get("href", ""),
                        # Optionally add more fields if available
                    }
                    alerts.append(alert)

                update_alerts(alerts)
                logger.info(f"✅ Fetched and updated {len(alerts)} disaster alerts.")
        except Exception as e:
            logger.warning(f"⚠️ Error fetching alerts: {e}")

        await asyncio.sleep(600)  # 10 mins
