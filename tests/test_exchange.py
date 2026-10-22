"""NBP response validation, money rounding and backward-compatible selection."""
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).parents[1] / 'custom_components/hohenwutzen_fuel'

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result

exchange = module('exchange')
display = module('display')


def payload(rate=4.25, day='2026-10-21'):
    return {'table': 'A', 'code': 'EUR', 'rates': [{'mid': rate, 'effectiveDate': day}]}


class ExchangeTests(unittest.TestCase):
    def test_reference_rate_direction(self):
        rate = exchange.parse_exchange_rate(payload())
        self.assertEqual(exchange.convert_price(1.52, rate.pln_per_eur), 6.46)
        self.assertEqual(rate.effective_date, '2026-10-21')

    def test_two_decimal_half_up_rounding(self):
        self.assertEqual(exchange.convert_price(1.50, 4.27), 6.41)

    def test_bad_quotes_rejected(self):
        for rate in (0, -4.0, float('nan'), float('inf'), True, '4.25', None):
            with self.subTest(rate=rate), self.assertRaises(exchange.ExchangeRateError):
                exchange.parse_exchange_rate(payload(rate))

    def test_wrong_currency_table_missing_and_multiple_rates(self):
        variants = [{}, None, {'table': 'B', 'code': 'EUR', 'rates': []},
                    {'table': 'A', 'code': 'USD', 'rates': []},
                    {'table': 'A', 'code': 'EUR', 'rates': []},
                    {'table': 'A', 'code': 'EUR', 'rates': payload()['rates'] * 2}]
        for data in variants:
            with self.subTest(data=data), self.assertRaises(exchange.ExchangeRateError):
                exchange.parse_exchange_rate(data)

    def test_invalid_publication_date(self):
        for day in ('2026-13-01', 'yesterday', '20261021', None):
            with self.subTest(day=day), self.assertRaises(exchange.ExchangeRateError):
                exchange.parse_exchange_rate(payload(day=day))

    def test_invalid_converted_value_is_not_a_price(self):
        for rate in (0, -1, float('nan'), None):
            with self.subTest(rate=rate), self.assertRaises(exchange.ExchangeRateError):
                exchange.convert_price(1.52, rate)

    def test_existing_entries_stay_in_eur(self):
        self.assertEqual(display.selected_profile({}, {}), 'de_eur')
        self.assertEqual(display.currency_for('de_eur'), 'EUR')
        self.assertEqual(display.price_unique_key('diesel', 'EUR'), 'diesel')

    def test_options_override_initial_selection(self):
        self.assertEqual(display.selected_profile({'display_profile': 'de_eur'}, {'display_profile': 'pl_pln'}), 'pl_pln')
        self.assertEqual(display.selected_profile({'display_profile': 'pl_pln'}, {'display_profile': 'de_eur'}), 'de_eur')

    def test_invalid_saved_profile_falls_back_to_original_eur(self):
        self.assertEqual(display.selected_profile({}, {'display_profile': 'invalid'}), 'de_eur')

    def test_pln_has_separate_history_and_polish_names(self):
        self.assertEqual(display.currency_for('pl_pln'), 'PLN')
        self.assertEqual(display.price_unique_key('diesel', 'PLN'), 'diesel_pln')
        self.assertEqual(display.NAMES['pl_pln']['diesel'], 'Olej napędowy')


if __name__ == '__main__':
    unittest.main()
