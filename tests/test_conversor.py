import unittest
from unittest.mock import patch

from Tools.pages.conversor import ConversorStategf
from tests.state_test_utils import build_state


def _base_state(**overrides):
    base = {
        "monto_convertido": "",
        "monto": "",
        "moneda_base": "",
        "moneda_destino": "",
        "tasa_cambio": "",
        "tmr_cop": "Cargando . . .",
    }
    base.update(overrides)
    return build_state(ConversorStategf, **base)


class ConversorTests(unittest.TestCase):
    def test_missing_fields_returns_validation_message(self):
        state = _base_state(monto="10")
        ConversorStategf.convertir_monedas.fn(state)
        self.assertEqual(state.monto_convertido, "Por favor, complete todos los campos.")

    def test_negative_amount_returns_validation_message(self):
        state = _base_state(monto="-5", moneda_base="USD", moneda_destino="COP")
        ConversorStategf.convertir_monedas.fn(state)
        self.assertEqual(state.monto_convertido, "El monto debe ser mayor que 0.")

    @patch("Tools.pages.conversor.obtener_tasa_cambio")
    def test_same_currency_skips_remote_lookup(self, mock_rate):
        state = _base_state(monto="25", moneda_base="USD", moneda_destino="USD")
        ConversorStategf.convertir_monedas.fn(state)
        self.assertIn("25.00 USD equivale a 25.00 USD", state.monto_convertido)
        self.assertEqual(state.tasa_cambio, "Tasa de cambio: 1.0000")
        mock_rate.assert_not_called()

    @patch("Tools.pages.conversor.obtener_tasa_cambio", return_value=4000.0)
    def test_successful_conversion(self, _mock_rate):
        state = _base_state(monto="2", moneda_base="USD", moneda_destino="COP")
        ConversorStategf.convertir_monedas.fn(state)
        self.assertIn("2.00 USD equivale a 8000.00 COP", state.monto_convertido)
        self.assertEqual(state.tasa_cambio, "Tasa de cambio: 4000.0000")

    @patch("Tools.pages.conversor.obtener_tasa_cambio", return_value="Error remoto")
    def test_remote_error_is_exposed(self, _mock_rate):
        state = _base_state(monto="2", moneda_base="USD", moneda_destino="COP")
        ConversorStategf.convertir_monedas.fn(state)
        self.assertEqual(state.monto_convertido, "No se pudo realizar la conversión.")
        self.assertEqual(state.tasa_cambio, "Error remoto")


if __name__ == "__main__":
    unittest.main()
