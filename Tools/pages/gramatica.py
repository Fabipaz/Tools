import reflex as rx
from spellchecker import SpellChecker


# Inicializar el corrector fuera de la clase de estado
corrector = SpellChecker(language='es')

class GramaticaState(rx.State):
    text_in: str = ''
    text_out: str = ''
    show_notification: bool = False

    def validacion(self):
        self.text_out = self.correct_text(self.text_in)

    def copy_text(self):
        self.show_notification = True
        return rx.set_clipboard(self.text_out)

    def correct_text(self, text):
        words = text.split()
        corrected_words = [
            corrector.correction(word) if corrector.correction(word) is not None else word
            for word in words
        ]
        return " ".join(corrected_words)


from Tools.components.navbar import navbar
from Tools.components.footer import footer

def gramatica() -> rx.Component:
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
                    "Corrector Ortográfico",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Corrige tus textos automáticamente.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Texto a corregir", class_name="font-semibold mb-2"),
                        rx.text_area(
                            placeholder="Escribe o pega tu texto aquí...",
                            on_change=GramaticaState.set_text_in,
                            value=GramaticaState.text_in,
                            size="3",
                            width="100%",
                            rows="6",
                        ),
                        class_name="mb-6",
                    ),

                    rx.el.button(
                        "Corregir Texto", 
                        on_click=GramaticaState.validacion,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),

                    rx.cond(
                        GramaticaState.text_out != "",
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Texto Corregido", class_name="text-sm text-gray-400 mb-2"),
                                rx.text_area(
                                    value=GramaticaState.text_out,
                                    read_only=True,
                                    size="3",
                                    width="100%",
                                    rows="6",
                                ),
                                rx.el.button(
                                    rx.icon("copy", size=20),
                                    on_click=GramaticaState.copy_text,
                                    class_name="absolute top-9 right-4 p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors",
                                ),
                                class_name="relative",
                            ),
                            rx.cond(
                                GramaticaState.show_notification,
                                rx.el.p(
                                    "¡Texto copiado al portapapeles!",
                                    class_name="text-green-400 text-sm mt-2 text-center",
                                ),
                                None
                            ),
                            class_name="w-full",
                        ),
                        None
                    ),
                    class_name="w-full max-w-3xl",
                ),

                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )