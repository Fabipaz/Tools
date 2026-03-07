import datetime
import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
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
