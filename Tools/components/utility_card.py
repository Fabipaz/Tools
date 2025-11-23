import reflex as rx


def utility_card(icon: str, title: str, description: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, size=28, class_name="text-[var(--accent-color-light)]"),
                class_name="p-4 bg-[var(--accent-color)]/10 rounded-xl border border-[var(--accent-color)]/20",
            ),
            rx.el.h3(title, class_name="mt-4 text-xl font-bold text-white"),
            rx.el.p(description, class_name="mt-2 text-sm text-gray-400"),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.div(
                "Use Tool",
                rx.icon("arrow-right", size=16, class_name="ml-2"),
                class_name="w-full flex items-center justify-center px-4 py-2 text-sm font-semibold text-white bg-[var(--accent-color)] group-hover:bg-[var(--accent-color-light)] rounded-lg transition-colors duration-300",
            ),
            class_name="mt-6",
        ),
        href=href,
        class_name="group flex flex-col h-full bg-[#1A1F3A] p-6 rounded-2xl border border-gray-700/50 hover:border-[var(--accent-color)]/50 transition-all duration-300 hover:shadow-[0_0_20px_var(--accent-color-light)] hover:-translate-y-1",
    )