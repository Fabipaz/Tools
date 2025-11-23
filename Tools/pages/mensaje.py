import reflex as rx


class MensajeState(rx.State):
    numero: str = ""
    error: str = ""
    mensaje_url: str = ""



    def enviar(self):
        if self.numero != "":
            self.mensaje_url = f"https://wa.me/57{self.numero}"
            self.error = ""
            return rx.call_script(f"window.open('{self.mensaje_url}', '_blank')")
        else:
            self.error = "Ingrese un número válido"
            self.mensaje_url = ""




from Tools.components.navbar import navbar
from Tools.components.footer import footer

def mensaje() -> rx.Component:
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
                    "Enviar Mensaje WhatsApp",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Envía un mensaje directo a un número de WhatsApp sin guardarlo.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Número de Teléfono", class_name="font-semibold mb-2"),
                        rx.el.div(
                            rx.el.span("+57", class_name="absolute left-3 top-3 text-gray-400 font-mono text-lg"),
                            rx.input(
                                placeholder="Ej: 3001234567",
                                on_change=MensajeState.set_numero,
                                value=MensajeState.numero,
                                size="3",
                                width="100%",
                            ),
                            class_name="relative",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Enviar Mensaje",
                        on_click=MensajeState.enviar,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                    rx.cond(
                        MensajeState.error != "",
                        rx.el.p(
                            MensajeState.error,
                            class_name="text-red-400 text-center font-semibold",
                        ),
                        None
                    ),
                    class_name="w-full max-w-xl",
                ),

                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )  