import asyncio
import httpx
import logging
from .routes import update_earthquakes, update_alerts

logger = logging.getLogger("flashrisk.fetchers")

# === APIs ===
USGS_API = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
RELIEFWEB_API = "https://api.reliefweb.int/v1/disasters?appname=FlashRisk&limit=20&sort[]=date:desc"

# === Called from FastAPI's startup ===
async def start_background_fetchers(app, notification_manager):
    asyncio.create_task(fetch_and_update_earthquakes())
    asyncio.create_task(fetch_and_update_alerts())
    logger.info("✔️ Earthquake and Alert background fetchers started")

# === Earthquake Fetcher ===
async def fetch_and_update_earthquakes():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(USGS_API, timeout=10)
                res.raise_for_status()
                data = res.json()

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

        await asyncio.sleep(600)  # 10 mins

# === Alert Fetcher ===
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

                    alert_type = (
                        fields["type"][0]["name"]
                        if "type" in fields and isinstance(fields["type"], list) and fields["type"]
                        else "Unknown"
                    )

                    country = (
                        fields["country"][0]["name"]
                        if "country" in fields and isinstance(fields["country"], list) and fields["country"]
                        else "Unknown"
                    )

                    alerts.append({
                        "id": str(d["id"]),
                        "type": alert_type,
                        "country": country,
                        "status": fields.get("status", "unknown"),
                        "date": fields.get("date", {}).get("created"),
                        "url": fields.get("url", "")
                    })

                update_alerts(alerts)
                logger.info(f"✅ Fetched and updated {len(alerts)} disaster alerts.")
        except Exception as e:
            logger.warning(f"⚠️ Error fetching alerts: {e}")

        await asyncio.sleep(600)  # 10 mins
