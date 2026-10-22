"""Test the actual station section separately from market/shop descriptions."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('parser', Path(__file__).parents[1]/'custom_components/hohenwutzen_fuel/parser.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)


def section(content):
    return '<h3>Tankstelle</h3>'+content+'<h3>Aktuelle Kraftstoffpreise</h3>'


class OpeningTests(unittest.TestCase):
    def test_operator_structure_is_open(self):
        self.assertIs(parser.parse_station_open(section('🕒 24/7 geöffnet🅿️ Gratis Parkplätze🚻 Kostenlose Toilette')), True)

    def test_explicit_closure(self):
        self.assertIs(parser.parse_station_open(section('Vorübergehend geschlossen.')), False)

    def test_closure_overrides_regular_hours(self):
        self.assertIs(parser.parse_station_open(section('24/7 geöffnet. Die Tankstelle ist aktuell geschlossen.')), False)

    def test_nested_markup(self):
        self.assertIs(parser.parse_station_open('<h3><span>Tankstelle</span></h3><b>24 / 7</b>&nbsp;geöffnet<h3>Preise</h3>'), True)

    def test_unrelated_hours_do_not_imply_station_is_open(self):
        for html in ('<h3>Polenmarkt</h3>24/7 geöffnet', section('24h-Shop'), '<h3>Tankstelle</h3>Keine Angaben<h3>Shop</h3>24/7 geöffnet'):
            with self.subTest(html=html):
                self.assertIsNone(parser.parse_station_open(html))

    def test_shop_closure_does_not_close_station(self):
        self.assertIs(parser.parse_station_open(section('24/7 geöffnet. Shop geschlossen.')), True)

    def test_missing_or_changed_schedule_is_unavailable(self):
        for html in ('Site unavailable', section('Montag bis Freitag 08–18 Uhr'), section('')):
            with self.subTest(html=html):
                self.assertIsNone(parser.parse_station_open(html))

    def test_script_status_ignored(self):
        self.assertIsNone(parser.parse_station_open(section('<script>24/7 geöffnet</script>')))

    def test_conflicting_station_sections_are_unavailable(self):
        self.assertIsNone(parser.parse_station_open(section('24/7 geöffnet')+section('Derzeit geschlossen')))


if __name__ == '__main__':
    unittest.main()
