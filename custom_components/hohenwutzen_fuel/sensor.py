"""Fuel prices in the selected display currency, plus fetch timestamp."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NAME, SOURCE_URL
from .display import CONVERSION_NOTES, NAMES, price_unique_key
from .exchange import NBP_URL, convert_price

FUELS = ("super_e10", "super_plus", "diesel")


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    async_add_entities([FuelSensor(coordinator, key) for key in FUELS]
                       + [FetchTimestamp(coordinator)])


class BaseSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, key, name):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_name = name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "polenmarkt")}, name=NAME, configuration_url=SOURCE_URL,
        )


class FuelSensor(BaseSensor):
    _attr_icon = "mdi:gas-station"
    _attr_suggested_display_precision = 2

    def __init__(self, coordinator, key):
        super().__init__(coordinator, price_unique_key(key, coordinator.currency),
                         NAMES[coordinator.language][key])
        self.key = key
        self._attr_native_unit_of_measurement = f"{coordinator.currency}/L"

    @property
    def available(self):
        if not super().available or self.coordinator.data is None:
            return False
        return (self.coordinator.currency == "EUR"
                or self.coordinator.data.get("exchange_rate") is not None)

    @property
    def native_value(self):
        if not self.available:
            return None
        data = self.coordinator.data
        eur_price = data["prices"][self.key]
        if self.coordinator.currency == "EUR":
            return eur_price
        return convert_price(eur_price, data["exchange_rate"].pln_per_eur)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        fetched_at = data.get("fetched_at")
        attrs = {"source": SOURCE_URL,
                 "last_successful_fetch": fetched_at.isoformat() if fetched_at else None,
                 "converted": self.coordinator.currency == "PLN"}
        if self.coordinator.currency == "PLN":
            quote = data.get("exchange_rate")
            attrs.update({"original_price_eur": data.get("prices", {}).get(self.key),
                          "exchange_rate_source": NBP_URL,
                          "pln_per_eur": quote.pln_per_eur if quote else None,
                          "exchange_rate_date": quote.effective_date if quote else None,
                          "note": CONVERSION_NOTES[self.coordinator.language]})
        else:
            # Preserve the original German attributes for existing automations.
            attrs.update({"quelle": SOURCE_URL,
                          "letzter_erfolgreicher_abruf": attrs["last_successful_fetch"],
                          "hinweis": "Webseitenpreis; Abrufzeit ist nicht die Preisänderungszeit."})
        return attrs


class FetchTimestamp(BaseSensor):
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator):
        super().__init__(coordinator, "last_fetch", NAMES[coordinator.language]["last_fetch"])

    @property
    def native_value(self):
        return self.coordinator.data["fetched_at"]
