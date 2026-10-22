"""Offline parser tests, independent of a Home Assistant installation."""
import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('parser', Path(__file__).parents[1]/'custom_components/hohenwutzen_fuel/parser.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

class ParserTests(unittest.TestCase):
    def test_published_text_structure(self):
        # Synthetic fixture based on the publicly retrieved source text, not raw live HTML.
        html='<h3>Aktuelle Kraftstoffpreise</h3><p>Super<span>1,52</span></p><p>Plus<span>1,68</span></p><p>Diesel<span>1,83</span></p><p>Tagesaktuelle Preise pro Liter in Euro.</p>'
        self.assertEqual(parser.parse_prices(html), {'super_e10':1.52, 'super_plus':1.68,'diesel':1.83})

    def test_markup_entities_and_three_decimals(self):
        html='Kraftstoffpreise <div>Super E10&nbsp;<b>1,</b><sup>529</sup></div> Super plus 1.689 Diesel 1,839 Tagesaktuelle Preise'
        self.assertEqual(parser.parse_prices(html)['super_e10'],1.529)

    def test_scripts_ignored(self):
        html='Kraftstoffpreise <script>Super 0,99 Plus 0,99 Diesel 0,99</script>Super 1,52 Plus 1,68 Diesel 1,83 Tagesaktuelle'
        self.assertEqual(parser.parse_prices(html)['diesel'],1.83)

    def test_reject_unavailable_missing_ambiguous_or_unreasonable(self):
        for board in ('Site Unavailable', 'Super 1,52 Plus 1,68',
                      'Super 1,52 Super 1,55 Plus 1,68 Diesel 1,83',
                      'Super 0,00 Plus 1,68 Diesel 1,83'):
            with self.subTest(board=board), self.assertRaises(parser.PriceParseError):
                parser.parse_prices('Kraftstoffpreise '+board+' Tagesaktuelle')

    def test_requires_price_board(self):
        with self.assertRaises(parser.PriceParseError):
            parser.parse_prices('Super 1,52 Plus 1,68 Diesel 1,83')

    def test_ignores_unrelated_marketing_prices(self):
        self.assertEqual(parser.parse_prices('Super E10 (ROZ 95) Plus Diesel Kraftstoffpreise Super 1,52 Plus 1,68 Diesel 1,83 Tagesaktuelle Autowäsche 3,90')['super_e10'],1.52)

if __name__=='__main__': unittest.main()
