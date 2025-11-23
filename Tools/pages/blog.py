import reflex as rx
from Tools.components.navbar import navbar
from Tools.components.footer import footer
from Tools.components.news_card import news_card

def blog() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Noticias & Actualizaciones",
                    class_name="text-4xl md:text-6xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Mantente al día con las últimas novedades tecnológicas.",
                    class_name="mt-4 text-lg text-gray-300 text-center max-w-2xl",
                ),
                class_name="container mx-auto flex flex-col items-center justify-center pt-24 pb-12 px-4",
            ),
            rx.el.div(
                rx.el.div(
                    news_card(
                        image="https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=2070&auto=format&fit=crop",
                        title="Introducción a Reflex: Desarrollo Web en Python",
                        date="Nov 23, 2024",
                        description="Descubre cómo crear aplicaciones web full-stack utilizando únicamente Python con Reflex.",
                        href="https://reflex.dev/blog/2024-03-21-reflex-0-4-0",
                    ),
                    news_card(
                        image="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop",
                        title="El Futuro de la Ciberseguridad",
                        date="Nov 20, 2024",
                        description="Tendencias y desafíos en la seguridad informática para el próximo año.",
                        href="https://www.cisa.gov/news-events/news",
                    ),
                    news_card(
                        image="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2070&auto=format&fit=crop",
                        title="Avances en Inteligencia Artificial",
                        date="Nov 18, 2024",
                        description="Cómo los nuevos modelos de lenguaje están transformando el desarrollo de software.",
                        href="https://openai.com/blog",
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
