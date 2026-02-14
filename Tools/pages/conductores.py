import reflex as rx
import math

class ConductorState(rx.State):
    # Inputs básicos
    potencia: str = ""
    voltaje: str = ""
    longitud: str = ""
    sistema: str = "monofasico"  # monofasico o trifasico
    material: str = "cobre"  # cobre o aluminio
    
    # Parámetros avanzados
    factor_potencia: str = "0.9"
    porcentaje_caida_max: str = "3"  # % máximo permitido
    
    # Resultados
    corriente: str = ""
    caida_tension: str = ""
    porcentaje_caida: str = ""
    seccion_calculada: str = ""
    calibre_recomendado: str = ""
    resultado: str = ""
    
    # Constantes de material (resistividad en Ω·mm²/m a 20°C)
    K_COBRE = 12.9
    K_ALUMINIO = 21.2
    
    # Multiplicadores de fase
    M_MONOFASICO = 2
    M_TRIFASICO = 1.732
    
    # Tabla de calibres AWG/MCM con sección transversal en mm²
    CALIBRES = [
        {"awg": "14", "seccion": 2.08},
        {"awg": "12", "seccion": 3.31},
        {"awg": "10", "seccion": 5.26},
        {"awg": "8", "seccion": 8.37},
        {"awg": "6", "seccion": 13.3},
        {"awg": "4", "seccion": 21.15},
        {"awg": "2", "seccion": 33.62},
        {"awg": "1/0", "seccion": 53.48},
        {"awg": "2/0", "seccion": 67.43},
        {"awg": "3/0", "seccion": 85.01},
        {"awg": "4/0", "seccion": 107.2},
        {"awg": "250 MCM", "seccion": 126.7},
        {"awg": "300 MCM", "seccion": 152},
        {"awg": "350 MCM", "seccion": 177.3},
        {"awg": "400 MCM", "seccion": 202.7},
        {"awg": "500 MCM", "seccion": 253.4},
    ]

    def limpiar_resultado(self):
        """Limpia todos los resultados cuando se modifican los inputs"""
        self.corriente = ""
        self.caida_tension = ""
        self.porcentaje_caida = ""
        self.seccion_calculada = ""
        self.calibre_recomendado = ""
        self.resultado = ""
    
    def set_potencia(self, value: str):
        self.potencia = value
        self.limpiar_resultado()
    
    def set_voltaje(self, value: str):
        self.voltaje = value
        self.limpiar_resultado()
    
    def set_longitud(self, value: str):
        self.longitud = value
        self.limpiar_resultado()
    
    def set_sistema(self, value: str):
        self.sistema = value
        self.limpiar_resultado()
    
    def set_material(self, value: str):
        self.material = value
        self.limpiar_resultado()
    
    def set_factor_potencia(self, value: str):
        self.factor_potencia = value
        self.limpiar_resultado()
    
    def set_porcentaje_caida_max(self, value: str):
        self.porcentaje_caida_max = value
        self.limpiar_resultado()

    def calcular_conductores(self):
        try:
            # Convertir valores de entrada
            potencia = float(self.potencia) if self.potencia else 0
            voltaje = float(self.voltaje) if self.voltaje else 0
            longitud = float(self.longitud) if self.longitud else 0
            fp = float(self.factor_potencia) if self.factor_potencia else 0.9
            caida_max = float(self.porcentaje_caida_max) if self.porcentaje_caida_max else 3
            
        except ValueError:
            self.resultado = "Por favor, ingrese valores numéricos válidos"
            return

        if potencia == 0 or voltaje == 0 or longitud == 0:
            self.resultado = "Por favor, complete todos los campos requeridos"
            return
        if potencia < 0 or voltaje < 0 or longitud < 0:
            self.resultado = "Los valores de potencia, voltaje y longitud deben ser mayores que 0"
            return
        if fp <= 0:
            self.resultado = "El factor de potencia debe ser mayor que 0"
            return
        if caida_max <= 0:
            self.resultado = "La caída de tensión máxima debe ser mayor que 0"
            return

        # 1. Calcular la corriente (I)
        if self.sistema == "monofasico":
            corriente = potencia / (voltaje * fp)
            M = self.M_MONOFASICO
        else:  # trifasico
            corriente = potencia / (math.sqrt(3) * voltaje * fp)
            M = self.M_TRIFASICO
        
        self.corriente = f"{corriente:.2f}"
        
        # 2. Determinar constante K según material
        K = self.K_COBRE if self.material == "cobre" else self.K_ALUMINIO
        
        # 3. Calcular la caída de tensión máxima permitida en voltios
        vd_max = (caida_max / 100) * voltaje
        if vd_max <= 0:
            self.resultado = "La caída de tensión máxima calculada no es válida"
            return
        
        # 4. Calcular la sección mínima del conductor (CM)
        # Fórmula: CM = (M × K × I × L) / VD
        # Donde CM está en milésimas circulares, convertimos a mm²
        seccion_mm2 = (M * K * corriente * longitud) / vd_max
        
        self.seccion_calculada = f"{seccion_mm2:.2f}"
        
        # 5. Buscar el calibre comercial más cercano (superior)
        calibre_seleccionado = None
        for calibre in self.CALIBRES:
            if calibre["seccion"] >= seccion_mm2:
                calibre_seleccionado = calibre
                break
        
        if calibre_seleccionado is None:
            # Si ningún calibre es suficiente, usar el más grande
            calibre_seleccionado = self.CALIBRES[-1]
            self.calibre_recomendado = f"{calibre_seleccionado['awg']} (ADVERTENCIA: Puede requerir conductores en paralelo)"
        else:
            self.calibre_recomendado = calibre_seleccionado['awg']
        
        # 6. Calcular la caída de tensión real con el calibre seleccionado
        vd_real = (M * K * corriente * longitud) / calibre_seleccionado["seccion"]
        porcentaje_real = (vd_real / voltaje) * 100
        
        self.caida_tension = f"{vd_real:.2f}"
        self.porcentaje_caida = f"{porcentaje_real:.2f}"
        
        # 7. Verificar si cumple con la normativa
        cumple = "✓ SÍ" if porcentaje_real <= caida_max else "✗ NO"
        
        # Construir resultado
        sistema_texto = "Monofásico" if self.sistema == "monofasico" else "Trifásico"
        material_texto = "Cobre" if self.material == "cobre" else "Aluminio"
        
        self.resultado = (
            f"RESULTADOS DEL CÁLCULO\n"
            f"{'='*50}\n\n"
            f"Sistema: {sistema_texto}\n"
            f"Material: {material_texto}\n\n"
            f"1. Corriente calculada: {corriente:.2f} A\n\n"
            f"2. Sección mínima requerida: {seccion_mm2:.2f} mm²\n\n"
            f"3. Calibre recomendado: {self.calibre_recomendado}\n"
            f"   Sección real: {calibre_seleccionado['seccion']} mm²\n\n"
            f"4. Caída de tensión:\n"
            f"   - Voltios: {vd_real:.2f} V\n"
            f"   - Porcentaje: {porcentaje_real:.2f}%\n"
            f"   - Máximo permitido: {caida_max}%\n\n"
            f"5. ¿Cumple normativa?: {cumple}\n"
        )

from Tools.components.navbar import navbar
from Tools.components.footer import footer

def conductores() -> rx.Component:
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
                    "Cálculo de Conductores Eléctricos",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Calcula la sección y calibre de conductores según la caída de tensión permitida.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                
                rx.el.div(
                    # Parámetros básicos
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Potencia (W)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 5000",
                                on_change=ConductorState.set_potencia,
                                value=ConductorState.potencia,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Voltaje (V)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 220",
                                on_change=ConductorState.set_voltaje,
                                value=ConductorState.voltaje,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Longitud (m)", class_name="font-semibold mb-2"),
                            rx.input(
                                placeholder="Ej: 50",
                                on_change=ConductorState.set_longitud,
                                value=ConductorState.longitud,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Sistema", class_name="font-semibold mb-2"),
                            rx.select(
                                ["monofasico", "trifasico"],
                                value=ConductorState.sistema,
                                on_change=ConductorState.set_sistema,
                                size="3",
                                width="100%",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Material", class_name="font-semibold mb-2"),
                            rx.select(
                                ["cobre", "aluminio"],
                                value=ConductorState.material,
                                on_change=ConductorState.set_material,
                                size="3",
                                width="100%",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                    ),

                    # Parámetros avanzados
                    rx.el.div(
                        rx.el.p("Parámetros Avanzados", class_name="text-xl font-bold text-white mb-4 mt-8"),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Factor de Potencia", class_name="font-semibold mb-2"),
                                rx.input(
                                    placeholder="0.9",
                                    on_change=ConductorState.set_factor_potencia,
                                    value=ConductorState.factor_potencia,
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p("Caída de Tensión Máxima (%)", class_name="font-semibold mb-2"),
                                rx.input(
                                    placeholder="3",
                                    on_change=ConductorState.set_porcentaje_caida_max,
                                    value=ConductorState.porcentaje_caida_max,
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        class_name="bg-[#1A1F3A]/30 p-6 rounded-xl border border-gray-700/30 mb-6",
                    ),

                    rx.el.button(
                        "Calcular Conductor", 
                        on_click=ConductorState.calcular_conductores,
                        class_name="w-full py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-6 cursor-pointer",
                    ),
                    
                    rx.cond(
                        ConductorState.resultado != "",
                        rx.el.div(
                            rx.el.p("Resultado", class_name="text-sm text-gray-400 mb-4"),
                            rx.el.pre(
                                ConductorState.resultado,
                                class_name="text-sm font-mono text-white whitespace-pre-wrap",
                            ),
                            class_name="bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
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
