"""Exercise production coordinator with mocked HTTP and Home Assistant boundaries."""
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1] / 'custom_components/hohenwutzen_fuel'
PACKAGE = '_fuel_coordinator_test'


def mod(name, **attrs):
    result = ModuleType(name)
    result.__dict__.update(attrs)
    return result


class HttpError(Exception):
    pass


class UpdateFailed(Exception):
    pass


class CoordinatorBase:
    def __init__(self, *args, **kwargs):
        pass


class Response:
    def __init__(self, payload=None, html=None, error=None):
        self.payload, self.html, self.error = payload, html, error

    async def __aenter__(self):
        if self.error:
            raise self.error
        return self

    async def __aexit__(self, *args):
        return False

    def raise_for_status(self):
        pass

    async def json(self):
        return self.payload

    async def text(self):
        return self.html


class Session:
    def __init__(self):
        self.responses, self.urls = [], []

    def get(self, url):
        self.urls.append(url)
        return self.responses.pop(0)


def load_coordinator(session, clock):
    package = mod(PACKAGE)
    package.__path__ = [str(ROOT)]
    stubs = {
        PACKAGE: package,
        'aiohttp': mod('aiohttp', ClientError=HttpError),
        'homeassistant': mod('homeassistant'),
        'homeassistant.helpers': mod('homeassistant.helpers'),
        'homeassistant.helpers.aiohttp_client': mod('client', async_get_clientsession=lambda hass: session),
        'homeassistant.helpers.update_coordinator': mod('coordinator', DataUpdateCoordinator=CoordinatorBase, UpdateFailed=UpdateFailed),
        'homeassistant.util': mod('util', dt=SimpleNamespace(utcnow=lambda: clock[0])),
    }
    with patch.dict(sys.modules, stubs):
        for name in ('const', 'display', 'exchange', 'parser', 'coordinator'):
            spec = importlib.util.spec_from_file_location(f'{PACKAGE}.{name}', ROOT / f'{name}.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
        return module.FuelCoordinator


def quote(rate=4.25):
    return {'table': 'A', 'code': 'EUR', 'rates': [{'mid': rate, 'effectiveDate': '2026-10-21'}]}

HTML = '<h3>Tankstelle</h3>24/7 geöffnet<h3>Kraftstoffpreise</h3>Super 1,52 Plus 1,68 Diesel 1,83 Tagesaktuelle Preise'


class RateCacheTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = Session()
        self.clock = [datetime(2026, 10, 22, 10, tzinfo=timezone.utc)]
        self.cls = load_coordinator(self.session, self.clock)

    def coordinator(self, profile='pl_pln'):
        return self.cls(None, SimpleNamespace(data={'display_profile': profile}, options={}))

    async def test_eur_does_not_call_nbp(self):
        c = self.coordinator('de_eur')
        self.session.responses = [Response(html=HTML)]
        data = await c._async_update_data()
        self.assertEqual(len(self.session.urls), 1)
        self.assertIsNone(data['exchange_rate'])
        self.assertEqual(data['prices']['diesel'], 1.83)

    async def test_language_does_not_select_currency_or_nbp_requests(self):
        for language in ('de', 'pl', 'en'):
            for currency in ('EUR', 'PLN'):
                with self.subTest(language=language, currency=currency):
                    c = self.cls(None, SimpleNamespace(
                        data={'display_profile': 'pl_pln'},
                        options={'language': language, 'currency': currency}))
                    self.session.urls = []
                    self.session.responses = [Response(html=HTML)]
                    if currency == 'PLN':
                        self.session.responses.append(Response(payload=quote()))
                    data = await c._async_update_data()
                    self.assertEqual((c.language, c.currency), (language, currency))
                    self.assertEqual(len(self.session.urls), 2 if currency == 'PLN' else 1)
                    self.assertEqual(data['exchange_rate'] is not None, currency == 'PLN')

    async def test_cache_and_hourly_refresh(self):
        c = self.coordinator()
        self.session.responses = [Response(payload=quote()), Response(payload=quote(4.30))]
        first = await c._async_exchange_rate()
        self.clock[0] += timedelta(minutes=59)
        self.assertIs(await c._async_exchange_rate(), first)
        self.assertEqual(len(self.session.urls), 1)
        self.clock[0] += timedelta(minutes=1)
        self.assertEqual((await c._async_exchange_rate()).pln_per_eur, 4.30)
        self.assertEqual(len(self.session.urls), 2)

    async def test_failed_refresh_clears_old_rate_and_recovers(self):
        c = self.coordinator()
        self.session.responses = [Response(payload=quote()), Response(error=HttpError('offline')), Response(payload=quote(4.30))]
        await c._async_exchange_rate()
        self.clock[0] += timedelta(hours=1)
        self.assertIsNone(await c._async_exchange_rate())
        self.assertIsNone(c._exchange_rate)
        self.assertEqual((await c._async_exchange_rate()).pln_per_eur, 4.30)

    async def test_bad_nbp_payload_is_not_used(self):
        c = self.coordinator()
        self.session.responses = [Response(payload={'code': 'USD'})]
        self.assertIsNone(await c._async_exchange_rate())

    async def test_fx_outage_keeps_station_status_and_raw_prices(self):
        c = self.coordinator()
        self.session.responses = [Response(html=HTML), Response(error=HttpError('offline'))]
        data = await c._async_update_data()
        self.assertIsNone(data['exchange_rate'])
        self.assertIs(data['station_open'], True)
        self.assertEqual(data['prices']['super_e10'], 1.52)
        self.assertIsNotNone(data['fetched_at'])


if __name__ == '__main__':
    unittest.main()
