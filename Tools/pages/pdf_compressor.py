from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path

import reflex as rx

from Tools.components.footer import footer
from Tools.components.navbar import navbar

UPLOAD_ID = "pdf_compressor_upload"
COMPRESSION_LEVELS = ["bajo", "medio", "alto"]


def _safe_filename(name: str, level: str) -> str:
    clean_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(name).stem).strip("._")
    if not clean_stem:
        clean_stem = "documento"
    return f"{clean_stem}_comprimido_{level}.pdf"


def _image_profile(level: str) -> tuple[int, int]:
    if level == "alto":
        return 800, 18
    if level == "medio":
        return 1200, 35
    return 1600, 55


def _compress_page_images(page, level: str) -> int:
    max_side, quality = _image_profile(level)
    replaced = 0
    for image_file in list(page.images):
        try:
            image = image_file.image
            if image is None:
                continue

            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            working = image.copy()
            working.thumbnail((max_side, max_side))

            # JPEG con calidad baja para máxima reducción de tamaño.
            image_file.replace(
                working,
                quality=quality,
                optimize=True,
                progressive=True,
                subsampling=2,
            )
            replaced += 1
        except Exception:
            # Si un recurso no se puede convertir, se conserva y se sigue.
            continue
    return replaced


def _compress_pdf_bytes(pdf_data: bytes, level: str) -> tuple[bytes, int]:
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception as exc:
        raise RuntimeError(
            "Falta la dependencia pypdf. Instala requirements.txt antes de usar esta utilidad."
        ) from exc

    try:
        import PIL  # noqa: F401
    except Exception as exc:
        raise RuntimeError(
            "Falta Pillow para comprimir imágenes agresivamente. Instala requirements.txt."
        ) from exc

    reader = PdfReader(BytesIO(pdf_data))
    writer = PdfWriter()
    replaced_images = 0

    for page in reader.pages:
        try:
            page.compress_content_streams()
        except Exception:
            # Algunos PDFs ya vienen optimizados o con streams no comprimibles.
            pass
        writer.add_page(page)
        replaced_images += _compress_page_images(writer.pages[-1], level)

    if level in {"medio", "alto"}:
        writer.add_metadata({"/Producer": "Reflex Tools PDF Compressor"})

    if level == "alto" and hasattr(writer, "compress_identical_objects"):
        try:
            writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
        except Exception:
            pass

    output = BytesIO()
    writer.write(output)
    return output.getvalue(), replaced_images


class PdfCompressorState(rx.State):
    compression_level: str = "medio"
    applied_level: str = ""
    images_processed: int = 0
    status: str = ""
    error: str = ""
    processing: bool = False
    source_filename: str = ""
    output_filename: str = ""
    original_size_mb: str = ""
    compressed_size_mb: str = ""
    reduction_percent: str = ""

    @rx.var
    def has_result(self) -> bool:
        return bool(self.output_filename)

    def set_level(self, value: str):
        if value in COMPRESSION_LEVELS:
            self.compression_level = value

    async def compress_pdf(self, files: list[rx.UploadFile]):
        self.processing = True
        self.error = ""
        self.status = ""
        self.output_filename = ""
        self.compressed_size_mb = ""
        self.reduction_percent = ""
        self.applied_level = ""
        self.images_processed = 0

        if not files:
            self.error = "Adjunta un PDF antes de comprimir."
            self.processing = False
            return

        upload = files[0]
        filename = upload.filename or "documento.pdf"
        self.source_filename = filename

        if not filename.lower().endswith(".pdf"):
            self.error = "Solo se permiten archivos con extensión .pdf"
            self.processing = False
            return

        try:
            source_data = await upload.read()
        except Exception as exc:
            self.error = f"No se pudo leer el archivo: {exc}"
            self.processing = False
            return

        if not source_data:
            self.error = "El archivo está vacío."
            self.processing = False
            return

        if not source_data.startswith(b"%PDF"):
            self.error = "El archivo no parece ser un PDF válido."
            self.processing = False
            return

        source_size = len(source_data)
        self.original_size_mb = f"{source_size / (1024 * 1024):.2f} MB"

        try:
            compressed_data, replaced_images = _compress_pdf_bytes(
                source_data, self.compression_level
            )
        except Exception as exc:
            self.error = (
                "No se pudo comprimir el PDF. Verifica que no esté protegido o corrupto. "
                f"Detalle: {exc}"
            )
            self.processing = False
            return

        if len(compressed_data) >= source_size:
            compressed_data = source_data
            self.status = (
                "Este PDF ya está muy optimizado. Se conserva el archivo original para descarga."
            )
        else:
            self.status = "Compresión finalizada. Descarga el nuevo PDF."

        output_name = _safe_filename(filename, self.compression_level)
        output_path = rx.get_upload_dir() / output_name
        output_path.write_bytes(compressed_data)

        compressed_size = len(compressed_data)
        reduction = max(0.0, (1 - (compressed_size / source_size)) * 100)

        self.output_filename = output_name
        self.compressed_size_mb = f"{compressed_size / (1024 * 1024):.2f} MB"
        self.reduction_percent = f"{reduction:.1f}%"
        self.applied_level = self.compression_level
        self.images_processed = replaced_images
        self.processing = False


def pdf_compressor() -> rx.Component:
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
                    "Compresor de PDF",
                    class_name="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[var(--accent-color-light)] to-[var(--secondary-accent)]",
                ),
                rx.el.p(
                    "Reduce el tamaño de PDFs pesados manteniendo buena legibilidad.",
                    class_name="mt-2 text-lg text-gray-300 max-w-2xl mb-8",
                ),
                rx.el.div(
                    rx.el.p("Nivel de compresión", class_name="font-semibold mb-2"),
                    rx.select(
                        COMPRESSION_LEVELS,
                        value=PdfCompressorState.compression_level,
                        on_change=PdfCompressorState.set_level,
                        class_name="w-full",
                    ),
                    rx.el.p(
                        "Bajo: cambios mínimos. Medio: balance recomendado. Alto: reducción máxima posible.",
                        class_name="mt-2 text-sm text-gray-400",
                    ),
                    class_name="mb-6 w-full max-w-2xl",
                ),
                rx.upload(
                    rx.el.div(
                        rx.icon("file-up", size=36, class_name="text-cyan-200"),
                        rx.el.p(
                            "Adjuntar PDF",
                            class_name="text-lg font-semibold text-white mt-2",
                        ),
                        rx.el.p(
                            "Haz clic o arrastra tu archivo aquí",
                            class_name="text-sm text-gray-400",
                        ),
                        class_name="flex flex-col items-center justify-center min-h-40 border-2 border-dashed border-gray-600 rounded-xl p-6",
                    ),
                    id=UPLOAD_ID,
                    accept={"application/pdf": [".pdf"]},
                    max_files=1,
                    multiple=False,
                    class_name="w-full max-w-2xl",
                ),
                rx.el.ul(
                    rx.foreach(
                        rx.selected_files(UPLOAD_ID),
                        lambda file: rx.el.li(
                            file, class_name="text-sm text-gray-300 list-disc ml-6 mt-2"
                        ),
                    ),
                    class_name="w-full max-w-2xl mb-6",
                ),
                rx.el.button(
                    "Comprimir PDF",
                    on_click=[
                        PdfCompressorState.compress_pdf(rx.upload_files(upload_id=UPLOAD_ID)),
                        rx.clear_selected_files(UPLOAD_ID),
                    ],
                    class_name="w-full max-w-2xl py-3 rounded-xl bg-gradient-to-r from-[var(--accent-color)] to-[var(--secondary-accent)] text-white font-bold text-lg hover:opacity-90 transition-opacity duration-200 mb-4 cursor-pointer",
                ),
                rx.cond(
                    PdfCompressorState.processing,
                    rx.el.p("Procesando archivo...", class_name="text-gray-300 mb-4"),
                    None,
                ),
                rx.cond(
                    PdfCompressorState.error != "",
                    rx.el.p(PdfCompressorState.error, class_name="text-red-400 mb-4"),
                    None,
                ),
                rx.cond(
                    PdfCompressorState.status != "",
                    rx.el.p(PdfCompressorState.status, class_name="text-emerald-300 mb-4"),
                    None,
                ),
                rx.cond(
                    PdfCompressorState.has_result,
                    rx.el.div(
                        rx.el.p(
                            f"Archivo: ",
                            rx.el.span(
                                PdfCompressorState.source_filename,
                                class_name="font-semibold",
                            ),
                            class_name="text-sm text-gray-300",
                        ),
                        rx.el.p(
                            "Tamaño original: ",
                            rx.el.span(
                                PdfCompressorState.original_size_mb,
                                class_name="font-semibold text-white",
                            ),
                            class_name="text-sm text-gray-300",
                        ),
                        rx.el.p(
                            "Tamaño comprimido: ",
                            rx.el.span(
                                PdfCompressorState.compressed_size_mb,
                                class_name="font-semibold text-white",
                            ),
                            class_name="text-sm text-gray-300",
                        ),
                        rx.el.p(
                            "Reducción: ",
                            rx.el.span(
                                PdfCompressorState.reduction_percent,
                                class_name="font-semibold text-emerald-300",
                            ),
                            class_name="text-sm text-gray-300 mb-4",
                        ),
                        rx.el.p(
                            "Nivel aplicado: ",
                            rx.el.span(
                                PdfCompressorState.applied_level,
                                class_name="font-semibold text-white",
                            ),
                            class_name="text-sm text-gray-300",
                        ),
                        rx.el.p(
                            "Imágenes recomprimidas: ",
                            rx.el.span(
                                PdfCompressorState.images_processed,
                                class_name="font-semibold text-white",
                            ),
                            class_name="text-sm text-gray-300 mb-4",
                        ),
                        rx.el.a(
                            "Descargar PDF comprimido",
                            href=rx.get_upload_url(PdfCompressorState.output_filename),
                            download=PdfCompressorState.output_filename,
                            class_name="inline-block px-5 py-3 rounded-lg bg-cyan-600 hover:bg-cyan-500 transition-colors text-white font-semibold",
                        ),
                        class_name="w-full max-w-2xl bg-[#1A1F3A]/50 p-6 rounded-xl border border-gray-700/50",
                    ),
                    None,
                ),
                class_name="container mx-auto flex flex-col px-4 pt-16 pb-8",
            ),
            class_name="flex-grow",
        ),
        footer(),
        class_name="flex flex-col min-h-screen",
    )
