import re
import time

import requests

_CACHE_TTL_SECONDS = 600
_cache: dict[tuple[str, str], tuple[float, float]] = {}


def _parse_number(text: str) -> float:
    clean = re.sub(r"[^0-9,\.]", "", text)
    if "," in clean and "." in clean:
        if clean.rfind(",") > clean.rfind("."):
            clean = clean.replace(".", "").replace(",", ".")
        else:
            clean = clean.replace(",", "")
    elif "," in clean:
        clean = clean.replace(",", ".")
    return float(clean)


def _fetch_google_finance(moneda_base: str, moneda_destino: str) -> float:
    url = f"https://www.google.com/finance/quote/{moneda_base}-{moneda_destino}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        )
    }

    response = requests.get(url, headers=headers, timeout=8)
    if response.status_code != 200:
        raise ValueError(f"Error HTTP {response.status_code} al obtener {moneda_base}-{moneda_destino}")

    match = re.search(
        r'class="YMlKec fxKbKc"[^>]*>\s*([^<]+)\s*<',
        response.text,
        flags=re.IGNORECASE,
    )
    if not match:
        raise ValueError(f"No se pudo encontrar la tasa de cambio para {moneda_base}-{moneda_destino}")

    return _parse_number(match.group(1))


def _fetch_open_er_api(moneda_base: str, moneda_destino: str) -> float:
    url = f"https://open.er-api.com/v6/latest/{moneda_base}"
    response = requests.get(url, timeout=8)
    if response.status_code != 200:
        raise ValueError(f"Error HTTP {response.status_code} en proveedor alterno")

    try:
        data = response.json()
    except Exception as exc:
        raise ValueError("Respuesta JSON invalida en proveedor alterno") from exc
    rates = data.get("rates", {})
    rate = rates.get(moneda_destino)
    if not isinstance(rate, (int, float)):
        raise ValueError(f"Proveedor alterno sin tasa para {moneda_base}-{moneda_destino}")
    return float(rate)


def _fetch_exchange_rate_host(moneda_base: str, moneda_destino: str) -> float:
    url = f"https://api.exchangerate.host/latest?base={moneda_base}&symbols={moneda_destino}"
    response = requests.get(url, timeout=8)
    if response.status_code != 200:
        raise ValueError(f"Error HTTP {response.status_code} en exchangerate.host")

    try:
        data = response.json()
    except Exception as exc:
        raise ValueError("Respuesta JSON invalida en exchangerate.host") from exc
    rates = data.get("rates", {})
    rate = rates.get(moneda_destino)
    if not isinstance(rate, (int, float)):
        raise ValueError(f"exchangerate.host sin tasa para {moneda_base}-{moneda_destino}")
    return float(rate)


def obtener_tasa_cambio(moneda_base: str, moneda_destino: str) -> float | str:
    key = (moneda_base.upper(), moneda_destino.upper())
    cached = _cache.get(key)
    now = time.time()
    if cached and (now - cached[1]) < _CACHE_TTL_SECONDS:
        return cached[0]

    errors: list[str] = []
    providers = (
        _fetch_google_finance,
        _fetch_open_er_api,
        _fetch_exchange_rate_host,
    )

    for provider in providers:
        try:
            tasa_cambio = provider(key[0], key[1])
            _cache[key] = (tasa_cambio, now)
            return tasa_cambio
        except (requests.RequestException, ValueError) as exc:
            errors.append(str(exc))

    joined_errors = " | ".join(errors) if errors else "sin detalle"
    return f"Error al obtener la tasa de cambio para {key[0]}-{key[1]}: {joined_errors}"
