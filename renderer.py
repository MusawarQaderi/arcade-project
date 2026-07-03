"""OLED rendering helpers for strict 128x64 / 8 px row layout."""

from config import Config


class Renderer:
    """Small display wrapper that keeps one show() call under app control."""

    # Tiny 5x7 block font for the boot logo. Original bitmap data, not a logo copy.
    BIG_FONT = {
        "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
        "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
        "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
        "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
        "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
        "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
        "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
        "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
        "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
        "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
        "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
        "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
        "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
        "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
        "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
        "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
        "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
        "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
        "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
        " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    }

    def __init__(self, display, config: Config) -> None:
        self.display = display
        self.config = config

    def clear(self) -> None:
        self.display.fill(0)

    def present(self) -> None:
        self.display.show()

    def row_y(self, row: int) -> int:
        if row < 0:
            return 0
        if row >= self.config.rows:
            return (self.config.rows - 1) * self.config.font_height
        return row * self.config.font_height

    def clip_text(self, text, max_chars: int) -> str:
        text = "" if text is None else str(text)
        if max_chars <= 0:
            return ""
        if len(text) <= max_chars:
            return text
        if max_chars <= 3:
            return text[:max_chars]
        return text[: max_chars - 3] + "..."

    def draw_text(self, text, x: int, y: int, color: int = 1, max_chars=None) -> None:
        if y < 0 or y > self.config.height - self.config.font_height:
            return
        if x < 0:
            skip = (-x + self.config.font_width - 1) // self.config.font_width
            text = str(text)[skip:]
            x = 0
        cols_left = (self.config.width - x) // self.config.font_width
        if max_chars is None or max_chars > cols_left:
            max_chars = cols_left
        clipped = self.clip_text(text, max_chars)
        if clipped:
            self.display.text(clipped, x, y, color)

    def draw_row(self, row: int, text, x: int = 0, color: int = 1, max_chars=None) -> None:
        self.draw_text(text, x, self.row_y(row), color, max_chars)

    def draw_centered_text(self, text, row: int, color: int = 1) -> None:
        clipped = self.clip_text(text, self.config.cols)
        x = max(0, (self.config.width - len(clipped) * self.config.font_width) // 2)
        self.draw_text(clipped, x, self.row_y(row), color, len(clipped))

    def draw_box(self, x: int, y: int, width: int, height: int, color: int = 1) -> None:
        if width <= 0 or height <= 0:
            return
        self.display.rect(x, y, width, height, color)

    def fill_box(self, x: int, y: int, width: int, height: int, color: int = 1) -> None:
        if width <= 0 or height <= 0:
            return
        if hasattr(self.display, "fill_rect"):
            self.display.fill_rect(x, y, width, height, color)
        else:
            for yy in range(y, y + height):
                self.display.line(x, yy, x + width - 1, yy, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int = 1) -> None:
        self.display.line(x1, y1, x2, y2, color)

    def draw_hline(self, y: int, color: int = 1) -> None:
        self.display.line(0, y, self.config.width - 1, y, color)

    def draw_vline(self, x: int, color: int = 1) -> None:
        self.display.line(x, 0, x, self.config.height - 1, color)

    def big_text_width(self, text, scale: int = 2, spacing: int = 1) -> int:
        width = 0
        for char in str(text).upper():
            glyph = self.BIG_FONT.get(char, self.BIG_FONT[" "])
            width += len(glyph[0]) * scale + spacing
        return max(0, width - spacing)

    def draw_big_text(self, text, x: int, y: int, scale: int = 2, color: int = 1, spacing: int = 1) -> None:
        x_pos = x
        for char in str(text).upper():
            glyph = self.BIG_FONT.get(char, self.BIG_FONT[" "])
            for row, bits in enumerate(glyph):
                yy = y + row * scale
                for col, bit in enumerate(bits):
                    if bit == "1":
                        self.fill_box(x_pos + col * scale, yy, scale, scale, color)
            x_pos += len(glyph[0]) * scale + spacing

    def draw_centered_big_text(self, text, y: int, scale: int = 2, color: int = 1) -> None:
        x = (self.config.width - self.big_text_width(text, scale)) // 2
        self.draw_big_text(text, x, y, scale, color)

    def draw_menu(self, title, items, selected: int, top: int = 0, owner: str = "") -> None:
        self.draw_centered_text(title, 0)
        self.draw_hline(9)
        visible_rows = 5
        if selected < top:
            top = selected
        if selected >= top + visible_rows:
            top = selected - visible_rows + 1
        for row in range(visible_rows):
            index = top + row
            y_row = row + 2
            if index >= len(items):
                self.draw_row(y_row, "")
                continue
            prefix = ">" if index == selected else " "
            label = self.clip_text(items[index], 13)
            self.draw_row(y_row, prefix + label, 0, 1, 16)
        if owner:
            self.draw_row(7, owner, 0, 1, 16)
