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


class _StationText(_Text):
    """Keep heading boundaries so shop/market hours cannot set station status."""

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if not self.skip and re.fullmatch(r"h[1-6]", tag):
            self.parts.append("\x1e")

    def handle_endtag(self, tag):
        if not self.skip and re.fullmatch(r"h[1-6]", tag):
            self.parts.append("\x1e")
        super().handle_endtag(tag)


def parse_station_open(html):
    """Return published station status, or None when it cannot be inferred.

    Only explicit closure or 24/7 opening in the Tankstelle section is supported.
    This is an operator website statement, not real-time operational telemetry.
    """
    parser = _StationText()
    parser.feed(html)
    text = " ".join(parser.parts)
    sections = re.findall(r"\x1e\s*Tankstelle\s*\x1e([^\x1e]*)", text, re.I)
    states = set()
    for section in sections:
        section = re.sub(r"\s+", " ", section)
        # A closure notice overrides regular 24/7 hours in the same section.
        if re.search(r"(?:\bTankstelle\s+(?:ist\s+)?|(?:^|[.!?])\s*)(?:(?:vorübergehend|derzeit|aktuell)\s+)?geschlossen\b", section, re.I):
            states.add(False)
        elif re.search(r"\b24\s*/\s*7\s+geöffnet\b", section, re.I):
            states.add(True)
        else:
            return None
    return states.pop() if len(states) == 1 else None
