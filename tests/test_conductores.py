import unittest

from Tools.pages.conductores import ConductorState
from tests.state_test_utils import build_state


def _base_state(**overrides):
    base = {
        "potencia": "5000",
        "voltaje": "220",
        "longitud": "50",
        "sistema": "monofasico",
        "material": "cobre",
        "factor_potencia": "0.9",
        "porcentaje_caida_max": "3",
        "corriente": "",
        "caida_tension": "",
        "porcentaje_caida": "",
        "seccion_calculada": "",
        "calibre_recomendado": "",
        "resultado": "",
    }
    base.update(overrides)
    state = build_state(ConductorState, **base)
    object.__setattr__(
        state,
        "CALIBRES",
        [
            {"awg": "14", "seccion": 2.08},
            {"awg": "12", "seccion": 3.31},
            {"awg": "10", "seccion": 5.26},
            {"awg": "8", "seccion": 8.37},
            {"awg": "6", "seccion": 13.3},
            {"awg": "4", "seccion": 21.15},
            {"awg": "2", "seccion": 33.62},
            {"awg": "1/0", "seccion": 53.48},
            {"awg": "2/0", "seccion": 67.43},
            {"awg": "3/0", "seccion": 85.01},
            {"awg": "4/0", "seccion": 107.2},
            {"awg": "250 MCM", "seccion": 126.7},
            {"awg": "300 MCM", "seccion": 152},
            {"awg": "350 MCM", "seccion": 177.3},
            {"awg": "400 MCM", "seccion": 202.7},
            {"awg": "500 MCM", "seccion": 253.4},
        ],
    )
    object.__setattr__(state, "K_COBRE", 12.9)
    object.__setattr__(state, "K_ALUMINIO", 21.2)
    object.__setattr__(state, "M_MONOFASICO", 2)
    object.__setattr__(state, "M_TRIFASICO", 1.732)
    return state


class ConductoresTests(unittest.TestCase):
    def test_factor_potencia_must_be_positive(self):
        state = _base_state(factor_potencia="0")
        ConductorState.calcular_conductores.fn(state)
        self.assertEqual(state.resultado, "El factor de potencia debe ser mayor que 0")

    def test_caida_maxima_must_be_positive(self):
        state = _base_state(porcentaje_caida_max="0")
        ConductorState.calcular_conductores.fn(state)
        self.assertEqual(
            state.resultado, "La caída de tensión máxima debe ser mayor que 0"
        )

    def test_valid_calculation_generates_recommendation(self):
        state = _base_state()
        ConductorState.calcular_conductores.fn(state)
        self.assertIn("RESULTADOS DEL CÁLCULO", state.resultado)
        self.assertTrue(state.calibre_recomendado)
        self.assertTrue(state.seccion_calculada)


if __name__ == "__main__":
    unittest.main()
