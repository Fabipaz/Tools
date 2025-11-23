import reflex as rx

class StorageState(rx.State):
    bitrate: str = ""
    qty_cam: str = ""
    qty_days: str = ""
    resultado: str = ""

    def calcular_almacenamiento(self):
        try:
            bitrate = float(self.bitrate) if self.bitrate else 0
            qty_cam = float(self.qty_cam) if self.qty_cam else 0
            qty_days = float(self.qty_days) if self.qty_days else 0
        except ValueError:
            self.resultado = "Por favor, ingrese valores numéricos válidos"
            return
        
        if bitrate == 0 or qty_cam == 0 or qty_days == 0:
            self.resultado = "Por favor, complete todos los campos"
            return
        
        # Cálculo: (bitrate_kbps * qty_cam * qty_days * 24h * 3600s) / (8 bits/byte * 1024^3 bytes/GB)
        almacenamiento_gb = (bitrate * qty_cam * qty_days * 24 * 3600) / (8 * 1024 * 1024 * 1024)
        almacenamiento_tb = almacenamiento_gb / 1024
        
        self.resultado = f"Capacidad requerida: {almacenamiento_gb:.2f} GB ({almacenamiento_tb:.2f} TB)"


from Tools.components.navbar import navbar
from Tools.components.footer import footer

def almacenamiento() -> rx.Component:
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
                    "Cálculo de Almacenamiento CCTV",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Calcula el espacio de almacenamiento necesario para tu sistema de videovigilancia.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Bitrate cámara (kbps)", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder="Bitrate (Kbps)",
                            type="number",
                            on_change=StorageState.set_bitrate,
                            value=StorageState.bitrate,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p("Número de cámaras", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder="Cantidad de cámaras",
                            type="number",
                            on_change=StorageState.set_qty_cam,
                            value=StorageState.qty_cam,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.p("Número de días", class_name="font-semibold mb-2"),
                        rx.input(
                            placeholder="Días de almacenamiento",
                            type="number",
                            on_change=StorageState.set_qty_days,
                            value=StorageState.qty_days,
                            size="3",
                            width="100%",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Calcular", 
                        on_click=StorageState.calcular_almacenamiento,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                    rx.cond(
                        StorageState.resultado != "",
                        rx.el.div(
                            rx.el.p("Resultado", class_name="text-sm text-gray-400"),
                            rx.el.p(
                                StorageState.resultado,
                                class_name="text-xl font-mono text-white",
                            ),
                            class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                        ),
                        None
                    ),
                    class_name="w-full max-w-2xl",
                ),

                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )