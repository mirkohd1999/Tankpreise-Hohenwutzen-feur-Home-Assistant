"""Display profiles, independent of Home Assistant."""
CONF_PROFILE = "display_profile"
DEFAULT_PROFILE = "de_eur"
PROFILE_LABELS = {"de_eur": "Deutsch → Euro (€)", "pl_pln": "Polski → Złoty (zł)"}
NAMES = {
    "de_eur": {"super_e10": "Super E10", "super_plus": "Super Plus", "diesel": "Diesel",
               "last_fetch": "Letzter erfolgreicher Abruf", "station_open": "Tankstelle"},
    "pl_pln": {"super_e10": "Benzyna 95 (E10)", "super_plus": "Benzyna 98", "diesel": "Olej napędowy",
               "last_fetch": "Ostatni udany odczyt", "station_open": "Stacja paliw"},
}


def selected_profile(data, options):
    """Old entries without a profile keep their original German/EUR behavior."""
    value = options.get(CONF_PROFILE, data.get(CONF_PROFILE, DEFAULT_PROFILE))
    return value if value in PROFILE_LABELS else DEFAULT_PROFILE


def currency_for(profile):
    return "PLN" if profile == "pl_pln" else "EUR"


def price_unique_key(key, currency):
    """Keep EUR identities; do not mix EUR and PLN history in one entity."""
    return f"{key}_pln" if currency == "PLN" else key
