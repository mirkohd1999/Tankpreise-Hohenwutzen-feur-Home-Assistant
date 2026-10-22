"""Validate NBP reference rates and convert EUR prices to PLN."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import math

NBP_URL = "https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json"


class ExchangeRateError(ValueError):
    """NBP response cannot be used for conversion."""


@dataclass(frozen=True)
class ExchangeRate:
    pln_per_eur: float
    effective_date: str


def parse_exchange_rate(payload):
    try:
        if payload["table"] != "A" or payload["code"] != "EUR":
            raise ExchangeRateError("Expected NBP table A, currency EUR")
        rates = payload["rates"]
        if not isinstance(rates, list) or len(rates) != 1:
            raise ExchangeRateError("Expected exactly one latest quotation")
        raw = rates[0]["mid"]
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ExchangeRateError("Invalid exchange rate")
        rate = float(raw)
        if not math.isfinite(rate) or rate <= 0:
            raise ExchangeRateError("Exchange rate must be finite and positive")
        effective = rates[0]["effectiveDate"]
        if not isinstance(effective, str) or date.fromisoformat(effective).isoformat() != effective:
            raise ExchangeRateError("Invalid rate publication date")
        return ExchangeRate(rate, effective)
    except (KeyError, IndexError, TypeError, ValueError, OverflowError) as err:
        raise ExchangeRateError("Invalid NBP EUR/PLN response") from err


def convert_price(eur_price, rate):
    """Multiply PLN per EUR; use decimal rounding for money displayed per litre."""
    try:
        value = Decimal(str(eur_price)) * Decimal(str(rate))
        if not value.is_finite() or value <= 0:
            raise ExchangeRateError("Invalid converted price")
        return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError, TypeError) as err:
        raise ExchangeRateError("Cannot convert EUR price to PLN") from err
