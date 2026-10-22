"""Poll the public source once for all sensors."""
import asyncio
from datetime import timedelta
import logging
import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from .const import NAME, SOURCE_URL, UPDATE_MINUTES
from .parser import parse_prices, PriceParseError

_LOGGER = logging.getLogger(__name__)

class FuelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER, name=NAME, config_entry=entry,
                         update_interval=timedelta(minutes=UPDATE_MINUTES))
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        try:
            async with asyncio.timeout(25):
                async with self.session.get(SOURCE_URL) as response:
                    response.raise_for_status()
                    html = await response.text()
                prices = parse_prices(html)
        except (aiohttp.ClientError, TimeoutError, UnicodeError, PriceParseError) as err:
            raise UpdateFailed(f"Kraftstoffpreise konnten nicht geladen werden: {err}") from err
        return {"prices": prices, "fetched_at": dt_util.utcnow()}
