import reflex as rx
import colorsys
import logging


class ColorConverterState(rx.State):
    hex_input: str = "#9D4EDD"
    error_message: str = ""

    @rx.event
    def set_hex_input(self, value: str):
        self.hex_input = value
        if not self.is_valid_hex:
            self.error_message = "Invalid HEX color format."
        else:
            self.error_message = ""

    @rx.var
    def is_valid_hex(self) -> bool:
        hex_val = self.hex_input.lstrip("#")
        if len(hex_val) not in (3, 6):
            return False
        try:
            int(hex_val, 16)
            return True
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return False

    @rx.var
    def rgb_output(self) -> str:
        if not self.is_valid_hex:
            return "N/A"
        hex_val = self.hex_input.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join([c * 2 for c in hex_val])
        return (
            f"rgb({', '.join([str(int(hex_val[i : i + 2], 16)) for i in (0, 2, 4)])})"
        )

    @rx.var
    def hsl_output(self) -> str:
        if not self.is_valid_hex:
            return "N/A"
        hex_val = self.hex_input.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join([c * 2 for c in hex_val])
        r, g, b = [int(hex_val[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return f"hsl({int(h * 360)}, {int(s * 100)}%, {int(l * 100)}%)"