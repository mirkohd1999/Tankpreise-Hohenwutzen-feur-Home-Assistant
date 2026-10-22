"""Show the published opening status of the fuel station."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NAME, SOURCE_URL
from .display import NAMES


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([StationOpenSensor(entry.runtime_data)])


class StationOpenSensor(CoordinatorEntity, BinarySensorEntity):
    """Open/closed according to the station section of the operator website."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:store"
    _attr_device_class = BinarySensorDeviceClass.OPENING
    _attr_unique_id = f"{DOMAIN}_station_open"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = NAMES[coordinator.profile]["station_open"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "polenmarkt")}, name=NAME,
            configuration_url=SOURCE_URL,
        )

    @property
    def available(self):
        return (super().available and self.coordinator.data is not None
                and self.coordinator.data.get("station_open") is not None)

    @property
    def is_on(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("station_open")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        fetched_at = data.get("fetched_at")
        return {"quelle": SOURCE_URL,
                "letzter_erfolgreicher_abruf": fetched_at.isoformat() if fetched_at else None,
                "hinweis": "Laut Betreiber-Webseite; kein Live-Betriebsstatus."}
