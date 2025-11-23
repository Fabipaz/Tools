import reflex as rx


class MagnitudState(rx.State):
    conversion_type: str = ""
    magnitud: str = ""
    factor_potencia: str = "0.8"
    resultado: str = ""
    constante: float = 1.34102

    @rx.var(cache=True)
    def resultado_computado(self) -> str:
        try:
            mag = float(self.magnitud) if self.magnitud else 0
            fp = float(self.factor_potencia) if self.factor_potencia else 0.8
        except ValueError:
            return "Por favor, ingrese valores numéricos válidos"
        
        if self.conversion_type == "Kw to KVA":
            if fp == 0:
                return "El factor de potencia no puede ser 0"
            return f"{mag} Kw es igual {mag / fp:.2f} KVA"
        elif self.conversion_type == "KVA to Kw":
            return f"{mag} KVA es igual {mag * fp:.2f} Kw"
        elif self.conversion_type == "Kw to HP":
            return f"{mag} Kw es igual {mag * self.constante:.2f} HP"
        elif self.conversion_type == "HP to Kw":
            return f"{mag} HP es igual {mag / self.constante:.2f} Kw"
        else:
            return "Elija una opción de conversión"

    def convert(self):
        self.resultado = self.resultado_computado


from Tools.components.navbar import navbar
from Tools.components.footer import footer

def magnitudes() -> rx.Component:
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
                    "Conversor de Magnitudes",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Convierte entre Kw, KVA y HP fácilmente.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Tipo de Conversión", class_name="font-semibold mb-2"),
                        rx.select(
                            ["Kw to KVA","KVA to Kw","Kw to HP","HP to Kw"],
                            placeholder="Elige una conversión",
                            on_change=MagnitudState.set_conversion_type,
                            class_name="w-full p-3 rounded-xl bg-[#1A1F3A] border border-gray-700/50 focus:border-[var(--accent-color)] focus:ring-2 focus:ring-[var(--accent-color)]/50 transition-all duration-300 text-lg font-mono text-white",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p("Valor a convertir", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder="Ingrese magnitud",
                            type="number",
                            on_change=MagnitudState.set_magnitud,
                            value=MagnitudState.magnitud,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p("Factor de Potencia (F.P)", class_name="font-semibold mb-2"),
                        rx.el.div(
                            rx.input(
                                placeholder="Factor de potencia (0-1)",
                                type="number",
                                on_change=MagnitudState.set_factor_potencia,
                                value=MagnitudState.factor_potencia,
                                size="3",
                                width="100%",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Convertir", 
                        on_click=MagnitudState.convert,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                    rx.cond(
                        MagnitudState.resultado != "",
                        rx.el.div(
                            rx.el.p("Resultado", class_name="text-sm text-gray-400"),
                            rx.el.p(
                                MagnitudState.resultado,
                                class_name="text-xl font-mono text-white",
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
    )