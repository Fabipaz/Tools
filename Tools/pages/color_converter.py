import reflex as rx
from Tools.components.navbar import navbar
from Tools.components.footer import footer
from Tools.states.color_converter_state import ColorConverterState


def color_converter() -> rx.Component:
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
                    "Color Converter",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Convert colors between HEX, RGB, and HSL.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Enter HEX Color", class_name="font-semibold mb-2"),
                        rx.input(
                            default_value=ColorConverterState.hex_input,
                            on_change=ColorConverterState.set_hex_input.debounce(300),
                            placeholder="#RRGGBB",
                            size="3",
                            width="100%",
                        ),
                        rx.cond(
                            ColorConverterState.error_message != "",
                            rx.el.p(
                                ColorConverterState.error_message,
                                class_name="text-red-400 text-sm mt-2",
                            ),
                            None,
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        style={"background_color": ColorConverterState.hex_input},
                        class_name="w-24 h-24 rounded-2xl border-4 border-gray-600 shadow-lg",
                    ),
                    class_name="flex items-center gap-6 my-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("RGB", class_name="text-sm text-gray-400"),
                        rx.el.p(
                            ColorConverterState.rgb_output,
                            class_name="text-2xl font-mono text-white",
                        ),
                        class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                    ),
                    rx.el.div(
                        rx.el.p("HSL", class_name="text-sm text-gray-400"),
                        rx.el.p(
                            ColorConverterState.hsl_output,
                            class_name="text-2xl font-mono text-white",
                        ),
                        class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-6",
                ),
                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )