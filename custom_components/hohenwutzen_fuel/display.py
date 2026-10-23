"""Independent language and currency choices, with legacy profile support."""
CONF_LANGUAGE = "language"
CONF_CURRENCY = "currency"
LANGUAGE_LABELS = {"de": "Deutsch", "pl": "Polski", "en": "English"}
CURRENCY_LABELS = {"EUR": "Euro (€)", "PLN": "Złoty (zł)"}
NAMES = {
    "en": {"super_e10": "Super E10", "super_plus": "Super Plus", "diesel": "Diesel",
           "last_fetch": "Last successful fetch", "station_open": "Fuel station"},
    "de": {"super_e10": "Super E10", "super_plus": "Super Plus", "diesel": "Diesel",
               "last_fetch": "Letzter erfolgreicher Abruf", "station_open": "Tankstelle"},
    "pl": {"super_e10": "Benzyna 95 (E10)", "super_plus": "Benzyna 98", "diesel": "Olej napędowy",
               "last_fetch": "Ostatni udany odczyt", "station_open": "Stacja paliw"},
}


def selected_display(data, options):
    """Preserve old profiles; explicit options override each setting separately."""
    legacy = options.get("display_profile", data.get("display_profile", "de_eur"))
    default_language, default_currency = ("pl", "PLN") if legacy == "pl_pln" else ("de", "EUR")
    language = options.get(CONF_LANGUAGE, data.get(CONF_LANGUAGE, default_language))
    currency = options.get(CONF_CURRENCY, data.get(CONF_CURRENCY, default_currency))
    return (language if language in LANGUAGE_LABELS else default_language,
            currency if currency in CURRENCY_LABELS else default_currency)


def price_unique_key(key, currency):
    """Keep EUR identities; do not mix EUR and PLN history in one entity."""
    return f"{key}_pln" if currency == "PLN" else key


CONVERSION_NOTES = {
    "de": "Umrechnung zum NBP-Mittelkurs; kein PLN-Zahlpreis der Tankstelle.",
    "pl": "Przeliczenie według średniego kursu NBP; nie jest to cena stacji w PLN.",
    "en": "Converted using the NBP mid-market rate; not the station's PLN payment price.",
}
