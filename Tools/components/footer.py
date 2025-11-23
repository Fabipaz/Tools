import reflex as rx
from Tools.styles import icon_button_style
import datetime

def footer() -> rx.Component:
    return rx.fragment(
        # Mobile Bottom Navigation
        rx.el.footer(
            rx.el.div(
                rx.el.a(
                    rx.icon("home", size=24),
                    rx.el.span("Home", class_name="text-xs font-medium"),
                    href="/",
                    style=icon_button_style(True),
                ),
                rx.el.a(
                    rx.icon("settings", size=24),
                    rx.el.span("Settings", class_name="text-xs font-medium"),
                    href="#",
                    style=icon_button_style(False),
                ),
                rx.el.a(
                    rx.icon("info", size=24),
                    rx.el.span("Info", class_name="text-xs font-medium"),
                    href="#",
                    style=icon_button_style(False),
                ),
                class_name="grid grid-cols-3 gap-4 w-full max-w-sm",
            ),
            class_name="fixed bottom-0 left-0 right-0 md:hidden bg-[#1A1F3A]/80 backdrop-blur-lg border-t border-gray-700/50 p-4 flex justify-center z-50",
        ),
        # Desktop Footer
        rx.el.footer(
            rx.el.div(
                rx.el.p(
                    f"© {datetime.datetime.now().year} Utility App. All Rights Reserved.",
                    class_name="text-sm text-gray-400",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.icon("github", size=20),
                        href="https://github.com/fabipaz",
                        class_name="text-gray-400 hover:text-white",
                    ),
                    # rx.el.a(
                    #     rx.icon("twitter", size=20),
                    #     href="#",
                    #     class_name="text-gray-400 hover:text-white",
                    # ),
                    rx.el.a(
                        rx.icon("linkedin", size=20),
                        href="https://www.linkedin.com/in/hectorfabianpastrana/",
                        class_name="text-gray-400 hover:text-white",
                    ),
                    class_name="flex items-center gap-6",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center",
            ),
            class_name="hidden md:flex h-16 border-t border-gray-700/50 w-full mt-auto",
        )
    )