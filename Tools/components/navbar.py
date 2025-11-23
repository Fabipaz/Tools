import reflex as rx
from Tools.utils.currency import obtener_tasa_cambio

class NavbarState(rx.State):
    tmr: str = "Cargando..."

    def get_tmr(self):
        tasa = obtener_tasa_cambio("USD", "COP")
        if isinstance(tasa, float):
            self.tmr = f"TRM: ${tasa:,.0f}"
        else:
            self.tmr = "TRM: N/A"

def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon(
                        "zap", size=28, class_name="text-[var(--secondary-accent)]"
                    ),
                    rx.el.span(
                        "UTILITY",
                        class_name="text-2xl font-black tracking-widest text-white ml-2",
                    ),
                    class_name="flex items-center",
                ),
                href="/",
            ),
            rx.el.div(
                rx.el.a(
                    "Tools",
                    href="/",
                    class_name="text-gray-300 hover:text-white transition-colors duration-300",
                ),
                rx.el.div(
                    rx.text(NavbarState.tmr, class_name="text-green-400 font-mono font-bold"),
                    class_name="flex items-center px-3 py-1 rounded-lg bg-[#1A1F3A] border border-green-500/30",
                ),
                rx.el.a(
                    "Blog",
                    href="/blog",
                    class_name="text-gray-300 hover:text-white transition-colors duration-300",
                ),
                class_name="hidden md:flex items-center gap-8 font-semibold",
            ),
            rx.el.button(
                rx.icon("menu", size=24),
                class_name="md:hidden text-gray-300 hover:text-white",
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-20",
        ),
        class_name="w-full bg-[#1A1F3A]/50 backdrop-blur-lg border-b border-gray-700/50 sticky top-0 z-50",
        on_mount=NavbarState.get_tmr,
    )