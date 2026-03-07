import reflex as rx
from Tools.components.footer import footer
from Tools.components.navbar import navbar


def settings() -> rx.Component:
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
                    "Settings",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Configura preferencias de la aplicación.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                rx.el.div(
                    rx.el.p(
                        "Próximamente: idioma, tema y preferencias de cálculo.",
                        class_name="text-gray-200",
                    ),
                    class_name="w-full max-w-3xl bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                ),
                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )
