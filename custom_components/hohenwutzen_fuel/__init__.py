"""Fuel prices published by Polenmarkt Hohenwutzen."""
from homeassistant.const import Platform
from .coordinator import FuelCoordinator

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass, entry):
    coordinator = FuelCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
