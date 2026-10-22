"""Poll fuel prices; retrieve NBP reference rates only in PLN mode."""
import asyncio
from datetime import timedelta
import logging
import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from .const import NAME, SOURCE_URL, UPDATE_MINUTES
from .display import selected_profile, currency_for
from .exchange import NBP_URL, parse_exchange_rate
from .parser import parse_prices, parse_station_open, PriceParseError

_LOGGER = logging.getLogger(__name__)


class FuelCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER, name=NAME, config_entry=entry,
                         update_interval=timedelta(minutes=UPDATE_MINUTES))
        self.session = async_get_clientsession(hass)
        self.profile = selected_profile(entry.data, entry.options)
        self.currency = currency_for(self.profile)
        self._exchange_rate = None
        self._exchange_fetched_at = None
        self._exchange_error = False

    async def _async_exchange_rate(self):
        now = dt_util.utcnow()
        if (self._exchange_rate is not None and self._exchange_fetched_at is not None
                and now - self._exchange_fetched_at < timedelta(hours=1)):
            return self._exchange_rate
        try:
            async with asyncio.timeout(15):
                async with self.session.get(NBP_URL) as response:
                    response.raise_for_status()
                    payload = await response.json()
                quote = parse_exchange_rate(payload)
        except (aiohttp.ClientError, TimeoutError, ValueError, UnicodeError) as err:
            if not self._exchange_error:
                _LOGGER.warning("NBP EUR/PLN rate unavailable; PLN prices unavailable: %s", err)
            self._exchange_error = True
            self._exchange_rate = None
            self._exchange_fetched_at = None
            return None
        if self._exchange_error:
            _LOGGER.info("NBP EUR/PLN rate available again")
        self._exchange_error = False
        self._exchange_rate = quote
        self._exchange_fetched_at = now
        return quote

    async def _async_update_data(self):
        try:
            async with asyncio.timeout(25):
                async with self.session.get(SOURCE_URL) as response:
                    response.raise_for_status()
                    html = await response.text()
                prices = parse_prices(html)
        except (aiohttp.ClientError, TimeoutError, UnicodeError, PriceParseError) as err:
            raise UpdateFailed(f"Kraftstoffpreise konnten nicht geladen werden: {err}") from err
        fetched_at = dt_util.utcnow()
        quote = await self._async_exchange_rate() if self.currency == "PLN" else None
        return {"prices": prices, "station_open": parse_station_open(html),
                "fetched_at": fetched_at, "exchange_rate": quote}
