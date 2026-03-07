import reflex as rx
from Tools.utils.currency import obtener_tasa_cambio


class NavbarState(rx.State):
    trm: str = "Cargando..."
    mobile_menu_open: bool = False

    def get_trm(self):
        tasa = obtener_tasa_cambio("USD", "COP")
        if isinstance(tasa, float):
            self.trm = f"TRM: ${tasa:,.0f}"
        else:
            self.trm = "TRM: N/A"

    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    def close_mobile_menu(self):
        self.mobile_menu_open = False


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
                    rx.text(
                        NavbarState.trm,
                        class_name="text-green-400 font-mono font-bold",
                    ),
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
                on_click=NavbarState.toggle_mobile_menu,
                class_name="md:hidden text-gray-300 hover:text-white",
            ),
            class_name="container mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-20",
        ),
        rx.cond(
            NavbarState.mobile_menu_open,
            rx.el.div(
                rx.el.div(
                    rx.text(
                        NavbarState.trm,
                        class_name="text-green-400 font-mono font-bold text-xs",
                    ),
                    class_name="mb-2 px-3 py-2 rounded-lg bg-[#0F1533] border border-green-500/30",
                ),
                rx.el.a(
                    "Tools",
                    href="/",
                    on_click=NavbarState.close_mobile_menu,
                    class_name="block py-2 text-gray-200 hover:text-white transition-colors duration-200",
                ),
                rx.el.a(
                    "Blog",
                    href="/blog",
                    on_click=NavbarState.close_mobile_menu,
                    class_name="block py-2 text-gray-200 hover:text-white transition-colors duration-200",
                ),
                class_name="md:hidden absolute top-full left-0 right-0 px-4 py-3 bg-[#1A1F3A]/95 backdrop-blur-lg border-b border-gray-700/50 z-50",
            ),
            None,
        ),
        class_name="relative w-full bg-[#1A1F3A]/50 backdrop-blur-lg border-b border-gray-700/50 sticky top-0 z-50",
        on_mount=NavbarState.get_trm,
    )
