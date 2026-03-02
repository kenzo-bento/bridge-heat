import json
import asyncio
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN, PLATFORMS, UPLOAD_INTERVAL, SAMPLE_INTERVAL, TEMP, HUMIDITY, PRESSURE
from .uploader import send_temperature

import logging
import sqlite3

_LOGGER = logging.getLogger(__name__)

_LOGGER.info("Integration loaded")

async def async_setup(hass: HomeAssistant, config):
    hass.data.setdefault(DOMAIN, {})
    return True

async def fetch_temperature(hass: HomeAssistant):
    def query_db():
        db_path = hass.config.path("home-assistant_v2.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Query: join states and metadata, filter sensors by unit in attributes
        query = f"""SELECT s.metadata_id, m.entity_id, a.shared_attrs, s.last_updated_ts
                    FROM states s
                    JOIN states_meta m 
                    ON s.metadata_id = m.metadata_id
                    JOIN state_attributes a
                    ON s.attributes_id = a.attributes_id
                    WHERE m.entity_id LIKE "sensor.bridge_heat"
                    AND s.last_updated_ts >= strftime('%s','now') - ?
                    ORDER BY s.metadata_id, s.last_updated_ts;"""

        cur.execute(query, (SAMPLE_INTERVAL,))
        rows = cur.fetchall()
        conn.close()

        results = []
        for r in rows:
            try:
                attrs = json.loads(r["shared_attrs"])
                temperature = float(attrs.get("temperature"))
            except (ValueError, TypeError, json.JSONDecodeError):
                continue  # skip bad rows

            results.append({
                "entity": r["entity_id"],
                "temperature": temperature,
                "time": datetime.utcfromtimestamp(r["last_updated_ts"]).strftime("%Y-%m-%d %H:%M:%S")
            })
        return results

    # Run blocking SQLite query in a separate thread for asynchronous function
    return await hass.async_add_executor_job(query_db)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info("Bridge Heat called")
    hass.data[DOMAIN][entry.entry_id] = {
        "samples" : []
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def upload_job(now):
        if entry.options.get(TEMP):
            samples = await fetch_temperature(hass)
            if not samples:
                _LOGGER.info("No Samples to Upload")
                return

            try:
                await send_temperature(samples)
                hass.data[DOMAIN][entry.entry_id]["samples"] = []

            except Exception as err:
                _LOGGER.error("Upload failed: %s", err)

    # Schedule periodically

    remove_upload = async_track_time_interval(
        hass,
        upload_job,
        timedelta(seconds=UPLOAD_INTERVAL),
    )

    hass.data[DOMAIN][entry.entry_id]["remove_upload"] = remove_upload
    return True


async def async_unload_entry(hass, entry):
    data = hass.data[DOMAIN].pop(entry.entry_id)

    if data.get("remove_upload"):
        data["remove_upload"]()

    return True

