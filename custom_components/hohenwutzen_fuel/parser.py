"""Parse visible prices; reject missing or ambiguous data."""
from html.parser import HTMLParser
import re

class PriceParseError(ValueError):
    """The source no longer exposes an unambiguous price board."""

class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

PATTERNS = {
    "super_e10": r"(?<![\w])Super(?:\s+E10)?",
    "super_plus": r"(?<![\w])(?:Super\s*plus|Plus)",
    "diesel": r"(?<![\w])Diesel",
}

def parse_prices(html):
    parser = _Text()
    parser.feed(html)
    text = re.sub(r"\s+", " ", " ".join(parser.parts))
    # Restrict matching to the site's price board, not surrounding marketing text.
    start = re.search(r"(?:Aktuelle\s+)?Kraftstoffpreise", text, re.I)
    if not start:
        raise PriceParseError("Keine Kraftstoffpreistafel gefunden")
    board = text[start.end():]
    end = re.search(r"Tagesaktuelle", board, re.I)
    if not end:
        raise PriceParseError("Ende der Preistafel nicht gefunden")
    board = board[:end.start()]
    result = {}
    for key, label in PATTERNS.items():
        matches = re.findall(label + r"\s*[:–-]?\s*(\d\s*[,.]\s*\d{2,3})(?!\d)", board, re.I)
        values = {float(re.sub(r"\s", "", value).replace(",", ".")) for value in matches}
        if len(values) != 1:
            raise PriceParseError(f"Preis fehlt oder ist mehrdeutig: {key}")
        value = values.pop()
        if not 0.2 <= value <= 5:
            raise PriceParseError(f"Unplausibler Literpreis: {key}")
        result[key] = value
    return result
