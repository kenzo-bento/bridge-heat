import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

print("__name__:", __name__)

async def send_temperature(samples: list[dict]):
    # Simulate async network I/O
    await asyncio.sleep(0)

    # Replace this with real DB/API logic
    _LOGGER.info(
        "Uploading %d temperature samples",
        len(samples),
    )

    _LOGGER.debug("Payload: %s", samples)

    with open("/config/bridge_heat_debug.txt", "a") as f:
        f.write(f"Uploaded {len(samples)}. Sending Temperature...\n")



