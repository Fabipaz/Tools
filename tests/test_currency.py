import unittest
from unittest.mock import patch

from Tools.utils import currency


class _Response:
    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text


class CurrencyTests(unittest.TestCase):
    def setUp(self):
        currency._cache.clear()

    def test_parse_number_us_and_eu_formats(self):
        self.assertEqual(currency._parse_number("1,234.56"), 1234.56)
        self.assertEqual(currency._parse_number("1.234,56"), 1234.56)

    @patch("Tools.utils.currency.requests.get")
    def test_obtener_tasa_cambio_uses_cache(self, mock_get):
        html = '<div class="YMlKec fxKbKc">$1,234.56</div>'
        mock_get.return_value = _Response(200, html)

        first = currency.obtener_tasa_cambio("usd", "cop")
        second = currency.obtener_tasa_cambio("USD", "COP")

        self.assertEqual(first, 1234.56)
        self.assertEqual(second, 1234.56)
        self.assertEqual(mock_get.call_count, 1)

    @patch("Tools.utils.currency.requests.get")
    def test_obtener_tasa_cambio_http_error(self, mock_get):
        mock_get.return_value = _Response(503, "")
        result = currency.obtener_tasa_cambio("USD", "COP")
        self.assertIn("Error HTTP 503", result)

    @patch("Tools.utils.currency.requests.get")
    def test_obtener_tasa_cambio_parse_error(self, mock_get):
        html = '<div class="YMlKec fxKbKc">not-a-number</div>'
        mock_get.return_value = _Response(200, html)
        result = currency.obtener_tasa_cambio("USD", "COP")
        self.assertIn("Error al obtener la tasa de cambio", result)


if __name__ == "__main__":
    unittest.main()
