"""Verify production entities for all independent language/currency choices."""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1] / 'custom_components/hohenwutzen_fuel'
PACKAGE = '_fuel_entity_test'


def module(name, **attrs):
    result = ModuleType(name)
    result.__dict__.update(attrs)
    return result


class CoordinatorEntity:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def available(self):
        return self.coordinator.last_update_success


class SensorDisplayTests(unittest.TestCase):
    def test_language_changes_names_without_changing_price_identity_or_unit(self):
        package = module(PACKAGE)
        package.__path__ = [str(ROOT)]
        stubs = {
            PACKAGE: package,
            'homeassistant': module('ha'),
            'homeassistant.components': module('components'),
            'homeassistant.components.sensor': module('sensor', SensorEntity=type('SensorEntity', (), {}),
                SensorDeviceClass=SimpleNamespace(TIMESTAMP='timestamp')),
            'homeassistant.components.binary_sensor': module('binary',
                BinarySensorEntity=type('BinarySensorEntity', (), {}),
                BinarySensorDeviceClass=SimpleNamespace(OPENING='opening')),
            'homeassistant.helpers': module('helpers'),
            'homeassistant.helpers.entity': module('entity', DeviceInfo=dict,
                EntityCategory=SimpleNamespace(DIAGNOSTIC='diagnostic')),
            'homeassistant.helpers.update_coordinator': module('coordinator', CoordinatorEntity=CoordinatorEntity),
        }
        loaded = {}
        with patch.dict(sys.modules, stubs):
            for name in ('const', 'display', 'exchange', 'sensor', 'binary_sensor'):
                spec = importlib.util.spec_from_file_location(f'{PACKAGE}.{name}', ROOT / f'{name}.py')
                loaded[name] = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = loaded[name]
                spec.loader.exec_module(loaded[name])
            identities = {}
            for language in ('de', 'pl'):
                for currency in ('EUR', 'PLN'):
                    with self.subTest(language=language, currency=currency):
                        coordinator = SimpleNamespace(language=language, currency=currency,
                            last_update_success=True,
                            data={'prices': {'super_e10': 1.52}, 'station_open': True,
                                  'fetched_at': datetime(2026, 10, 22, tzinfo=timezone.utc),
                                  'exchange_rate': loaded['exchange'].ExchangeRate(4.25, '2026-10-21')})
                        price = loaded['sensor'].FuelSensor(coordinator, 'super_e10')
                        station = loaded['binary_sensor'].StationOpenSensor(coordinator)
                        self.assertEqual(price._attr_name, 'Super E10' if language == 'de' else 'Benzyna 95 (E10)')
                        self.assertEqual(price._attr_native_unit_of_measurement, f'{currency}/L')
                        self.assertEqual(price.native_value, 1.52 if currency == 'EUR' else 6.46)
                        self.assertEqual(station._attr_name, 'Tankstelle' if language == 'de' else 'Stacja paliw')
                        self.assertTrue(station.is_on)
                        if currency in identities:
                            self.assertEqual(price._attr_unique_id, identities[currency])
                        identities[currency] = price._attr_unique_id
            self.assertNotEqual(identities['EUR'], identities['PLN'])
