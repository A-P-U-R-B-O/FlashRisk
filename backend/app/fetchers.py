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

                    # Strictly require type and country to be present and not empty
                    alert_type = (
                        fields["type"][0]["name"]
                        if "type" in fields and isinstance(fields["type"], list) and fields["type"] and "name" in fields["type"][0]
                        else None
                    )
                    country = (
                        fields["country"][0]["name"]
                        if "country" in fields and isinstance(fields["country"], list) and fields["country"] and "name" in fields["country"][0]
                        else None
                    )

                    if not alert_type or not country:
                        logger.warning(f"Skipping alert with missing type/country (id={d.get('id')})")
                        continue

                    alert = {
                        "id": str(d["id"]),
                        "type": alert_type,
                        "country": country,
                        "status": fields.get("status", "unknown") or "unknown",
                        "date": fields.get("date", {}).get("created"),
                        "url": fields.get("url", "") or ""
                    }
                    alerts.append(alert)

                update_alerts(alerts)
                logger.info(f"✅ Fetched and updated {len(alerts)} disaster alerts.")
        except Exception as e:
            logger.warning(f"⚠️ Error fetching alerts: {e}")

        await asyncio.sleep(600)  # 10 mins
