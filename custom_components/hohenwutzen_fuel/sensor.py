"""Three price sensors and a successful-fetch timestamp."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NAME, SOURCE_URL

FUELS = (("super_e10", "Super E10"), ("super_plus", "Super Plus"), ("diesel", "Diesel"))

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    async_add_entities([FuelSensor(coordinator, key, name) for key, name in FUELS]
                       + [FetchTimestamp(coordinator)])

class BaseSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, key, name):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_name = name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "polenmarkt")},
            name=NAME, entry_type=None, configuration_url=SOURCE_URL,
        )

class FuelSensor(BaseSensor):
    _attr_native_unit_of_measurement = "EUR/L"
    _attr_icon = "mdi:gas-station"
    _attr_suggested_display_precision = 2

    def __init__(self, coordinator, key, name):
        super().__init__(coordinator, key, name)
        self.key = key

    @property
    def native_value(self):
        return self.coordinator.data["prices"][self.key]

    @property
    def extra_state_attributes(self):
        return {"quelle": SOURCE_URL,
                "letzter_erfolgreicher_abruf": self.coordinator.data["fetched_at"].isoformat(),
                "hinweis": "Webseitenpreis; Abrufzeit ist nicht die Preisänderungszeit."}

class FetchTimestamp(BaseSensor):
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator):
        super().__init__(coordinator, "last_fetch", "Letzter erfolgreicher Abruf")

    @property
    def native_value(self):
        return self.coordinator.data["fetched_at"]
