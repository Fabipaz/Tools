import reflex as rx
from Tools.utils.currency import obtener_tasa_cambio

class ConversorStategf(rx.State):
    monto_convertido: str = ""
    monto: str = ""
    moneda_base: str = ""
    moneda_destino: str = ""
    tasa_cambio: str = ""
    tmr_cop: str ="Cargando . . ."

    def convertir_monedas(self):
        if not self.monto or not self.moneda_base or not self.moneda_destino:
            self.monto_convertido = "Por favor, complete todos los campos."
            self.tasa_cambio = ""
            return
        try:
            monto_float = float(self.monto)
        except ValueError:
            self.monto_convertido = "Por favor, ingrese un monto válido."
            self.tasa_cambio = ""
            return

        if monto_float <= 0:
            self.monto_convertido = "El monto debe ser mayor que 0."
            self.tasa_cambio = ""
            return

        if self.moneda_base == self.moneda_destino:
            self.monto_convertido = (
                f"{monto_float:.2f} {self.moneda_base} equivale a "
                f"{monto_float:.2f} {self.moneda_destino}"
            )
            self.tasa_cambio = "Tasa de cambio: 1.0000"
            return

        tasa_cambio = obtener_tasa_cambio(self.moneda_base, self.moneda_destino)
        if isinstance(tasa_cambio, float):
            monto_convertido = monto_float * tasa_cambio
            self.monto_convertido = (
                f"{monto_float:.2f} {self.moneda_base} equivale a "
                f"{monto_convertido:.2f} {self.moneda_destino}"
            )
            self.tasa_cambio = f"Tasa de cambio: {tasa_cambio:.4f}"
        else:
            self.monto_convertido = "No se pudo realizar la conversión."
            self.tasa_cambio = str(tasa_cambio)

    def obtener_tmr_cop(self):
            self.tmr_cop = "0"
            tasa = obtener_tasa_cambio("USD", "COP")
            if isinstance(tasa, float):
                self.tmr_cop = f"{tasa:.2f}"
            else:
                self.tmr_cop = "Error"


from Tools.components.navbar import navbar
from Tools.components.footer import footer

def conversorgf() -> rx.Component:
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
                    "Conversor de Monedas",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Consulta la TMR y convierte entre diferentes monedas.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                # TMR Display
                rx.el.div(
                    rx.el.p("TMR (USD -> COP)", class_name="text-sm text-gray-400"),
                    rx.el.div(
                        rx.icon("dollar-sign", size=24, class_name="text-green-400 mr-2"),
                        rx.el.p(
                            ConversorStategf.tmr_cop,
                            class_name="text-2xl font-mono text-white",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50 mb-8 w-full max-w-2xl",
                ),

                # Conversion Form
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Monto", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder="Monto a Cambiar",
                            type="number",
                            value=ConversorStategf.monto,
                            on_change=ConversorStategf.set_monto,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("De", class_name="font-semibold mb-2"),
                            rx.select(
                                ["USD", "EUR", "GBP", "COP"],
                                placeholder="Moneda de origen",
                                value=ConversorStategf.moneda_base,
                                on_change=ConversorStategf.set_moneda_base,
                                class_name="w-full p-3 rounded-xl bg-[#1A1F3A] border border-gray-700/50 focus:border-[var(--accent-color)] focus:ring-2 focus:ring-[var(--accent-color)]/50 transition-all duration-300 text-lg font-mono text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("A", class_name="font-semibold mb-2"),
                            rx.select(
                                ["USD", "EUR", "GBP", "COP"],
                                placeholder="Moneda de destino",
                                value=ConversorStategf.moneda_destino,
                                on_change=ConversorStategf.set_moneda_destino,
                                class_name="w-full p-3 rounded-xl bg-[#1A1F3A] border border-gray-700/50 focus:border-[var(--accent-color)] focus:ring-2 focus:ring-[var(--accent-color)]/50 transition-all duration-300 text-lg font-mono text-white",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                    ),
                    rx.el.button(
                        "Convertir",
                        on_click=ConversorStategf.convertir_monedas,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                     rx.cond(
                        ConversorStategf.monto_convertido != "",
                        rx.el.div(
                            rx.el.p("Resultado", class_name="text-sm text-gray-400"),
                            rx.el.p(
                                ConversorStategf.monto_convertido,
                                class_name="text-xl font-mono text-white",
                            ),
                             rx.el.p(
                                ConversorStategf.tasa_cambio,
                                class_name="text-sm text-gray-500 mt-1",
                            ),
                            class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                        ),
                        None
                    ),
                    class_name="w-full max-w-2xl",
                ),

                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
        on_mount=ConversorStategf.obtener_tmr_cop,
    )
