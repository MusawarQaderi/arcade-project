"""Display rendering helpers for the arcade console."""

from config import Config


class Renderer:
    """Small wrapper around the display object."""

    def __init__(self, display, config: Config) -> None:
        self.display = display
        self.config = config

    def clear(self) -> None:
        self.display.fill(0)

    def draw_text(self, text: str, x: int, y: int, color: int = 1) -> None:
        self.display.text(text, x, y, color)

    def draw_centered_text(self, text: str, y: int, color: int = 1) -> None:
        x = max(0, (self.config.width - len(text) * 8) // 2)
        self.display.text(text, x, y, color)

    def draw_box(self, x: int, y: int, width: int, height: int, color: int = 1) -> None:
        self.display.rect(x, y, width, height, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: int = 1) -> None:
        self.display.line(x1, y1, x2, y2, color)

    def present(self) -> None:
        self.display.show()