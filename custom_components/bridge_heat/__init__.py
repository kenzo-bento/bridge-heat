import json
import asyncio
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval

from .const import *
from .uploader import send_data

import logging
import sqlite3

_LOGGER = logging.getLogger(__name__)

_LOGGER.info("Integration loaded")

async def async_setup(hass: HomeAssistant, config):
    hass.data.setdefault(DOMAIN, {})
    return True

async def fetch_data(hass: HomeAssistant, entry: ConfigEntry):
    def query_db():
        dicts = []
        if entry.options.get(TEMP):
            dicts.append(TEMP_ATTR)
        if entry.options.get(PRESSURE):
            dicts.append(PRESSURE_ATTR)
        if entry.options.get(HUMIDITY):
            dicts.append(HUMIDITY_ATTR)
        if entry.options.get(AQ):
            dicts.append(AQ_ATTR)
        if entry.options.get(ENERGY):
            dicts.append(ENERGY_ATTR)
        if entry.options.get(HVAC):
            dicts.append(HVAC_ATTR)
        if entry.options.get(LIGHT):
            dicts.append(LIGHT_ATTR)
        if entry.options.get(NOISE):
            dicts.append(NOISE_ATTR)
        
        DICT = {}
        for d in dicts:
            for k, v in d.items():
                DICT.setdefault(k, []).append(v)

        db_path = hass.config.path("home-assistant_v2.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        CLAUSE = " OR ".join([f"m.entity_id LIKE ?" for _ in DICT['name']])
        names = [DICT['name']]
        device_class = [DICT['device_class']]
        units = list(DICT['units_of_measurement'])
        params_prelim = names + device_class + units + [[SAMPLE_INTERVAL]]
        params = [item for sublist in params_prelim for item in sublist]
        # Query: join states and metadata, filter sensors by unit in attributes
        query = f"""SELECT s.state, s.metadata_id, m.entity_id, a.shared_attrs, s.last_updated_ts
                FROM states s
                JOIN states_meta m 
                ON s.metadata_id = m.metadata_id
                JOIN state_attributes a
                ON s.attributes_id = a.attributes_id
                WHERE (
                    {CLAUSE}
                    OR json_extract(a.shared_attrs, '$.device_class') IN ({','.join(['?'] * len(DICT['device_class']))})
                    OR json_extract(a.shared_attrs, '$.unit_of_measurement') IN ({','.join(['?'] * sum(len(sublist) for sublist in DICT['units_of_measurement']))})
                )
                AND s.last_updated_ts >= strftime('%s','now') - ?
                ORDER BY s.metadata_id, s.last_updated_ts;"""
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        results = []
        for r in rows:
            try:
                attrs = json.loads(r["shared_attrs"])
            except (ValueError, TypeError, json.JSONDecodeError):
                continue
            state = str(r["state"])

            results.append({
                "entity": r["entity_id"],
                "attributes": attrs,
                "state": state,
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
        samples = await fetch_data(hass, entry)
        if not samples:
            _LOGGER.info("No Samples to Upload")
            return

        try:
            await send_data(samples)
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

