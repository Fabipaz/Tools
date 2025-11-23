import reflex as rx
import math

class UpState(rx.State):
    carga: str = ""
    capacidad_ups: str = ""
    autonomia: str = ""
    voltaje: str = ""
    eficiencia: str = "0.9"   # Eficiencia inversor (default 90%)
    dod: str = "0.5"          # Profundidad de descarga (50% default para plomo-ácido)
    factor_seguridad: str = "1.1"  # Margen 10% extra
    voltaje_bateria: str = "12"    # Voltaje por batería individual
    capacidad_bateria: str = ""

    def calcular_banco_baterias(self):
        try:
            # Datos
            autonomia = float(self.autonomia)       # horas
            voltaje = float(self.voltaje)           # Vdc del banco
            eficiencia = float(self.eficiencia)     # eficiencia inversor
            dod = float(self.dod)                   # profundidad descarga
            k = float(self.factor_seguridad)        # factor de seguridad
            vbat = float(self.voltaje_bateria)      # V por batería
            carga = float(self.carga) if self.carga else 0
            autonomia = float(self.autonomia) if self.autonomia else 0
            voltaje = float(self.voltaje) if self.voltaje else 0
            eficiencia = float(self.eficiencia) if self.eficiencia else 0.9
            dod = float(self.dod) if self.dod else 0.5
            factor_seguridad = float(self.factor_seguridad) if self.factor_seguridad else 1.1
            voltaje_bateria = float(self.voltaje_bateria) if self.voltaje_bateria else 12
        except ValueError:
            self.resultado = "Por favor, ingrese valores numéricos válidos"
            return

        if carga == 0 or autonomia == 0 or voltaje == 0:
            self.resultado = "Por favor, complete todos los campos requeridos"
            return

        # Cálculo de capacidad de batería
        capacidad_ah = (carga * autonomia) / (voltaje * eficiencia * dod) * factor_seguridad
        
        # Cálculo de configuración de baterías
        if voltaje_bateria > 0:
            baterias_serie = math.ceil(voltaje / voltaje_bateria)
            baterias_paralelo = 1  # Simplificado
            num_baterias_total = baterias_serie * baterias_paralelo
            
            self.capacidad_bateria = f"{capacidad_ah:.2f}"
            self.num_baterias = str(num_baterias_total)
            self.baterias_serie = str(baterias_serie)
            self.baterias_paralelo = str(baterias_paralelo)
            
            self.resultado = (
                f"Capacidad requerida: {capacidad_ah:.2f} Ah\n"
                f"Configuración: {baterias_serie} baterías en serie × {baterias_paralelo} en paralelo\n"
                f"Total de baterías: {num_baterias_total}"
            )
        else:
            self.capacidad_bateria = f"{capacidad_ah:.2f}"
            self.resultado = f"Capacidad requerida: {capacidad_ah:.2f} Ah"

from Tools.components.navbar import navbar
from Tools.components.footer import footer

def ups() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", size=20, class_name="mr-2"),
                    "Back to Tools",
                    href="/",
                    class_name="flex items-center text-sm text-gray-400 hover:text-white transition-colors duration-200 mb-8",
                ),
                rx.el.h1(
                    "Cálculo Banco de Baterías UPS",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Calcula la capacidad y configuración necesaria para tu banco de baterías.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Carga (Watts)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 1000",
                                on_change=UpState.set_carga,
                                value=UpState.carga,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Capacidad UPS (kVA)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 3",
                                on_change=UpState.set_capacidad_ups,
                                value=UpState.capacidad_ups,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Autonomía (Horas)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 2",
                                on_change=UpState.set_autonomia,
                                value=UpState.autonomia,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Voltaje Banco (V)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 48",
                                on_change=UpState.set_voltaje,
                                value=UpState.voltaje,
                                size="3",
                                width="100%",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                    ),

                    rx.el.div(
                        rx.el.p("Parámetros Avanzados", class_name="text-xl font-bold text-white mb-4 mt-8"),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Eficiencia (0-1)", class_name="font-semibold mb-2"),
                                rx.input(
                                    placeholder="0.9",
                                    on_change=UpState.set_eficiencia,
                                    value=UpState.eficiencia,
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p("Profundidad Descarga", class_name="font-semibold mb-2"),
                                rx.input(
                                    placeholder="0.5",
                                    on_change=UpState.set_dod,
                                    value=UpState.dod,
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p("Factor Seguridad", class_name="font-semibold mb-2"),
                                rx.input(
                                    placeholder="1.1",
                                    on_change=UpState.set_factor_seguridad,
                                    value=UpState.factor_seguridad,
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p("Voltaje Batería (V)", class_name="font-semibold mb-2"),
                                rx.input(
                                    placeholder="12",
                                    on_change=UpState.set_voltaje_bateria,
                                    value=UpState.voltaje_bateria,
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        class_name="bg-[#1A1F3A]/30 p-6 rounded-xl border border-gray-700/30 mb-6",
                    ),

                    rx.el.button(
                        "Calcular Banco de Baterías", 
                        on_click=UpState.calcular_banco_baterias,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                    rx.cond(
                        UpState.capacidad_bateria != "",
                        rx.el.div(
                            rx.el.p("Resultado", class_name="text-sm text-gray-400"),
                            rx.el.pre(
                                UpState.capacidad_bateria,
                                class_name="text-xl font-mono text-white whitespace-pre-wrap",
                            ),
                            class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                        ),
                        None
                    ),
                    class_name="w-full max-w-3xl",
                ),

                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )