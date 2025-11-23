import reflex as rx

class OhmState(rx.State):
    voltaje: str = ""
    valor_variable: str = ""
    corriente_options: list[str] = ["Amperios", "Miliamperios", "Microamperios"]
    resistencia_options: list[str] = ["Ω", "KΩ", "MΩ"]
    select_unidad_option: str = ""
    resultado: str = ""
    conversion_type: str = ""

    @rx.var
    def resultado_ohm(self) -> str:
        try:
            v = float(self.voltaje) if self.voltaje else 0
            val = float(self.valor_variable) if self.valor_variable else 0
        except ValueError:
            return "Por favor, ingrese valores numéricos válidos"
        
        if self.conversion_type == "Calcular valor de la corriente":
            if v == 0 or val == 0:
                return "Por favor, ingrese valores válidos"
            corriente = v / val
            if self.select_unidad_option == "Amperios":
                return f"La corriente es igual a {corriente:.2f} A"
            elif self.select_unidad_option == "Miliamperios":
                return f"La corriente es igual a {corriente * 1000:.2f} mA"
            elif self.select_unidad_option == "Microamperios":
                return f"La corriente es igual a {corriente * 1000000:.2f} µA"
        elif self.conversion_type == "Calcular valor de la resistencia":
            if v == 0 or val == 0:
                return "Por favor, ingrese valores válidos"
            resistencia = v / val
            if self.select_unidad_option == "Ω":
                return f"La resistencia es igual a {resistencia:.2f} Ω"
            elif self.select_unidad_option == "KΩ":
                return f"La resistencia es igual a {resistencia / 1000:.2f} KΩ"
            elif self.select_unidad_option == "MΩ":
                return f"La resistencia es igual a {resistencia / 1000000:.2f} MΩ"
        elif self.conversion_type == "Calcular valor del voltaje":
            if v == 0 or val == 0:
                return "Por favor, ingrese valores válidos"
            return f"El voltaje es igual a {v * val:.2f} V"
        else:
            return "Elija una opción de conversión"

    @rx.var
    def placeholder_uno(self) -> str:
        if self.conversion_type == "Calcular valor de la corriente" or self.conversion_type == "Calcular valor de la resistencia":
            return "Ingrese el valor del voltaje"
        elif self.conversion_type == "Calcular valor del voltaje":
            return "Ingrese el valor de la corriente"
        return "Ingrese el valor"

    @rx.var
    def placeholder_dos(self) -> str:
        if self.conversion_type == "Calcular valor de la corriente":
            return "Ingrese el valor de la resistencia"
        elif self.conversion_type == "Calcular valor de la resistencia":
            return "Ingrese el valor de la corriente"
        elif self.conversion_type == "Calcular valor del voltaje":
            return "Ingrese el valor de la resistencia"
        return "Ingrese el valor"

    def convert(self):
        self.resultado = self.resultado_ohm


from Tools.components.navbar import navbar
from Tools.components.footer import footer

def ohm() -> rx.Component:
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
                    "Calculadora Ley de Ohm",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Calcula voltaje, corriente o resistencia fácilmente.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Tipo de Cálculo", class_name="font-semibold mb-2"),
                        rx.select(
                            ["Calcular valor de la corriente", "Calcular valor de la resistencia", "Calcular valor del voltaje"],
                            placeholder="Elige una conversión",
                            on_change=OhmState.set_conversion_type,
                            class_name="w-full p-3 rounded-xl bg-[#1A1F3A] border border-gray-700/50 focus:border-[var(--accent-color)] focus:ring-2 focus:ring-[var(--accent-color)]/50 transition-all duration-300 text-lg font-mono text-white",
                        ),
                        class_name="mb-4",
                    ),
                    
                    rx.cond(
                        OhmState.conversion_type == "Calcular valor de la corriente",
                        rx.el.div(
                            rx.el.p("Unidad de Corriente", class_name="font-semibold mb-2"),
                            rx.select(
                                OhmState.corriente_options,
                                placeholder="Seleccione unidad de corriente",
                                on_change=OhmState.set_select_unidad_option,
                                class_name="w-full p-3 rounded-xl bg-[#1A1F3A] border border-gray-700/50 focus:border-[var(--accent-color)] focus:ring-2 focus:ring-[var(--accent-color)]/50 transition-all duration-300 text-lg font-mono text-white",
                            ),
                            class_name="mb-4",
                        ),
                    ),
                    rx.cond(
                        OhmState.conversion_type == "Calcular valor de la resistencia",
                        rx.el.div(
                            rx.el.p("Unidad de Resistencia", class_name="font-semibold mb-2"),
                            rx.select(
                                OhmState.resistencia_options,
                                placeholder="Seleccione unidad de resistencia",
                                on_change=OhmState.set_select_unidad_option,
                                class_name="w-full p-3 rounded-xl bg-[#1A1F3A] border border-gray-700/50 focus:border-[var(--accent-color)] focus:ring-2 focus:ring-[var(--accent-color)]/50 transition-all duration-300 text-lg font-mono text-white",
                            ),
                            class_name="mb-4",
                        ),
                    ),

                    rx.el.div(
                        rx.el.p("Variable 1", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder=OhmState.placeholder_uno,
                            type="number",
                            on_change=OhmState.set_voltaje,
                            value=OhmState.voltaje,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p("Variable 2", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder=OhmState.placeholder_dos,
                            type="number",
                            on_change=OhmState.set_valor_variable,
                            value=OhmState.valor_variable,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-6",
                    ),

                    rx.el.button(
                        "Convertir", 
                        on_click=OhmState.convert,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                    rx.cond(
                        OhmState.resultado != "",
                        rx.el.div(
                            rx.el.p("Resultado", class_name="text-sm text-gray-400"),
                            rx.el.p(
                                OhmState.resultado,
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