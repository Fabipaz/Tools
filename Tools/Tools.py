import reflex as rx
from Tools.styles import STYLES
from Tools.components.navbar import navbar
from Tools.components.footer import footer
from Tools.components.utility_card import utility_card
from Tools.pages.color_converter import color_converter
from Tools.pages.conversor import conversorgf
from Tools.pages.almacenamiento import almacenamiento
from Tools.pages.magnitudes import magnitudes
from Tools.pages.mensaje import mensaje
from Tools.pages.ohm import ohm
from Tools.pages.ups import ups
from Tools.pages.gramatica import gramatica
from Tools.pages.conductores import conductores
from Tools.pages.blog import blog

def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Utilidades web para ingenieros",
                    class_name="text-4xl md:text-6xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Tu futuro conjunto de herramientas esenciales para ingenieros.",
                    class_name="mt-4 text-lg text-gray-300 text-center max-w-2xl",
                ),
                class_name="container mx-auto flex flex-col items-center justify-center pt-24 pb-12 px-4",
            ),
            rx.el.div(
                rx.el.div(
                    utility_card(
                        icon="palette",
                        title="Color Converter",
                        description="Convert colors between HEX, RGB, and HSL formats.",
                        href="/color-converter",
                    ),
                    utility_card(
                        icon="dollar-sign",
                        title="Monedas",
                        description="Convertir monedas.",
                        href="/monedas",
                    ),
                    utility_card(
                        icon="hard-drive",
                        title="Almacenamiento",
                        description="Calcula el almacenamiento necesario para CCTV.",
                        href="/almacenamiento",
                    ),
                    utility_card(
                        icon="cable",
                        title="Magnitudes",
                        description="Conversión de Kw, KVA y HP.",
                        href="/magnitudes",
                    ),
                    utility_card(
                        icon="message-circle",
                        title="Mensaje",
                        description="Envia un mensaje por WhatsApp.",
                        href="/mensaje",
                    ),
                    utility_card(
                        icon="plug-zap",
                        title="Ley de Ohm",
                        description="Calcula corriente, resistencia o voltaje.",
                        href="/ohm",
                    ),
                    utility_card(
                        icon="battery-charging",
                        title="Cálculo UPS",
                        description="Calcula banco de baterías para UPS.",
                        href="/ups",
                    ),
                    utility_card(
                        icon="book-open-check",
                        title="Ortografía",
                        description="Valida ortografía.",
                        href="/gramatica",
                    ),
                    utility_card(
                        icon="wires",
                        title="Conductores",
                        description="Calcula conductores para cables.",
                        href="/conductores",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full",
                ),
                class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )

app = rx.App(
    style=STYLES,
    theme=rx.theme(appearance="light", accent_color="purple"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
            rel="stylesheet",
        ),
    ],
)

# Add the pages to the app
app.add_page(index, route="/")
app.add_page(color_converter, route="/color-converter")
app.add_page(conversorgf, route="/monedas")
app.add_page(almacenamiento, route="/almacenamiento")
app.add_page(magnitudes, route="/magnitudes")
app.add_page(mensaje, route="/mensaje")
app.add_page(ohm, route="/ohm")
app.add_page(ups, route="/ups")
app.add_page(gramatica, route="/gramatica")
app.add_page(conductores, route="/conductores")
app.add_page(blog, route="/blog")
