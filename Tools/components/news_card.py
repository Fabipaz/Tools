import reflex as rx

def news_card(image: str, title: str, date: str, description: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.image(
                src=image,
                class_name="w-full h-48 object-cover rounded-t-xl",
            ),
            rx.el.div(
                rx.el.p(date, class_name="text-xs text-[var(--accent-color-light)] font-semibold mb-2"),
                rx.el.h3(title, class_name="text-xl font-bold text-white mb-2 line-clamp-2"),
                rx.el.p(description, class_name="text-sm text-gray-400 line-clamp-3"),
                class_name="p-6 flex-grow",
            ),
            rx.el.div(
                rx.el.div(
                    "Leer Más",
                    rx.icon("external-link", size=16, class_name="ml-2"),
                    class_name="w-full flex items-center justify-center px-4 py-2 text-sm font-semibold text-white bg-[var(--accent-color)] group-hover:bg-[var(--accent-color-light)] rounded-lg transition-colors duration-300",
                ),
                class_name="p-6 pt-0 mt-auto",
            ),
            class_name="flex flex-col h-full",
        ),
        href=href,
        target="_blank",
        class_name="group flex flex-col h-full bg-[#1A1F3A] rounded-2xl border border-gray-700/50 hover:border-[var(--accent-color)]/50 transition-all duration-300 hover:shadow-[0_0_20px_var(--accent-color-light)] hover:-translate-y-1 overflow-hidden",
    )
