import asyncio
import aiohttp
import logging
from .const import URL, KEY

_LOGGER = logging.getLogger(__name__)

print("__name__:", __name__)

async def send_data(samples: list[dict]):
    headers = {
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    valid_samples = []
    for s in samples:
        try:
            valid_samples.append(s)
        except (ValueError, TypeError):
            continue

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(URL, json=valid_samples, headers=headers) as resp:
                if resp.status == 201 or resp.status == 200:
                    result = await resp.json()
                else:
                    text = await resp.text()
        except Exception as e:
            pass
    # Simulate async network I/O
    await asyncio.sleep(0)



