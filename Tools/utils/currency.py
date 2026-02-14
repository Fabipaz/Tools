import re
import time

import requests
from bs4 import BeautifulSoup

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


def obtener_tasa_cambio(moneda_base: str, moneda_destino: str) -> float | str:
    key = (moneda_base.upper(), moneda_destino.upper())
    cached = _cache.get(key)
    now = time.time()
    if cached and (now - cached[1]) < _CACHE_TTL_SECONDS:
        return cached[0]

    url = f"https://www.google.com/finance/quote/{key[0]}-{key[1]}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code != 200:
            return f"Error HTTP {response.status_code} al obtener {key[0]}-{key[1]}"

        soup = BeautifulSoup(response.text, "html.parser")
        tasa_element = soup.find("div", class_="YMlKec fxKbKc")
        if not tasa_element:
            return f"No se pudo encontrar la tasa de cambio para {key[0]}-{key[1]}"

        tasa_cambio = _parse_number(tasa_element.text)
        _cache[key] = (tasa_cambio, now)
        return tasa_cambio
    except (requests.RequestException, ValueError):
        return f"Error al obtener la tasa de cambio para {key[0]}-{key[1]}"
