import asyncio
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN, PLATFORMS, UPLOAD_INTERVAL, SAMPLE_INTERVAL
from .uploader import send_temperature

import logging

_LOGGER = logging.getLogger(__name__)

_LOGGER.info("Integration loaded")

async def async_setup(hass: HomeAssistant, config):
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info("Bridge Heat called")
    hass.data[DOMAIN][entry.entry_id] = {
        "samples" : []
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if not entry.data.get("Permission to send Temperature Data", False):
        _LOGGER.info("Upload disabled by user permission")
        return True

    async def sample_job(now):
        _LOGGER.info("Sample job fired at %s", now)
        try:
            state = hass.states.get("weather.forecast_home") #replace with actual sensor
            if state is None or state.state in ("unknown", "unavailable"):
                _LOGGER.warning("Data is unavailable.")
                return
            temp = state.attributes.get("temperature")
            if temp is None:
                return
            hass.data[DOMAIN][entry.entry_id]["samples"].append({
                "timestamp": now.isoformat(),
                "temperature": float(temp),
            })
            with open("/config/bridge_heat_debug.txt", "a") as f:
                f.write(f"{now.isoformat()} - Sample job fired, temperature: {temp}\n")

        except Exception as err:
            _LOGGER.error("Sampling failed: %s", err)
            with open("/config/bridge_heat_debug.txt", "a") as f:
                f.write(f"{now.isoformat()} - Sample job FAILED: {err}\n")

    async def upload_job(now):
        samples = hass.data[DOMAIN][entry.entry_id]["samples"]
        if not samples:
            with open("/config/bridge_heat_debug.txt", "a") as f:
                f.write(f"{now.isoformat()} - No samples to upload\n")
            _LOGGER.info("No Samples to Upload")
            return

        try:
            await send_temperature(samples)
            hass.data[DOMAIN][entry.entry_id]["samples"] = []

            with open("/config/bridge_heat_debug.txt", "a") as f:
                f.write(f"{now.isoformat()} - Uploaded {len(samples)} samples\n")

        except Exception as err:
            _LOGGER.error("Upload failed: %s", err)
            with open("/config/bridge_heat_debug.txt", "a") as f:
                f.write(f"{now.isoformat()} - Upload FAILED: {err}\n")

    # Schedule every 15 minutes
    remove_sample = async_track_time_interval(
        hass,
        sample_job,
        timedelta(seconds=SAMPLE_INTERVAL),)

    remove_upload = async_track_time_interval(
        hass,
        upload_job,
        timedelta(seconds=UPLOAD_INTERVAL),
    )

    hass.data[DOMAIN][entry.entry_id]["remove_sample"] = remove_sample
    hass.data[DOMAIN][entry.entry_id]["remove_upload"] = remove_upload
    return True


async def async_unload_entry(hass, entry):
    data = hass.data[DOMAIN].pop(entry.entry_id)

    if data.get("remove_sample"):
        data["remove_sample"]()

    if data.get("remove_upload"):
        data["remove_upload"]()

    return True

