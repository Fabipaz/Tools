import unittest

from Tools.pages.ups import UpState
from tests.state_test_utils import build_state


def _base_state(**overrides):
    base = {
        "carga": "1000",
        "capacidad_ups": "3",
        "autonomia": "2",
        "voltaje": "48",
        "eficiencia": "0.9",
        "dod": "0.5",
        "factor_seguridad": "1.1",
        "voltaje_bateria": "12",
        "capacidad_bateria": "",
        "resultado": "",
        "num_baterias": "",
        "baterias_serie": "",
        "baterias_paralelo": "",
    }
    base.update(overrides)
    return build_state(UpState, **base)


class UpsTests(unittest.TestCase):
    def test_invalid_efficiency(self):
        state = _base_state(eficiencia="1.5")
        UpState.calcular_banco_baterias.fn(state)
        self.assertEqual(state.resultado, "La eficiencia debe estar entre 0 y 1")

    def test_invalid_dod(self):
        state = _base_state(dod="0")
        UpState.calcular_banco_baterias.fn(state)
        self.assertEqual(
            state.resultado, "La profundidad de descarga debe estar entre 0 y 1"
        )

    def test_valid_result_includes_ups_usage(self):
        state = _base_state(carga="900", capacidad_ups="3")
        UpState.calcular_banco_baterias.fn(state)
        self.assertIn("Capacidad requerida:", state.resultado)
        self.assertIn("Uso de UPS:", state.resultado)
        self.assertIn("30.0%", state.resultado)

    def test_overload_shows_warning(self):
        state = _base_state(carga="4500", capacidad_ups="3")
        UpState.calcular_banco_baterias.fn(state)
        self.assertIn("ADVERTENCIA UPS", state.resultado)


if __name__ == "__main__":
    unittest.main()
