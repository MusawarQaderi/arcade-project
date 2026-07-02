"""Minimal menu rendering and navigation."""


class MenuManager:
    """Handles a small vertical menu for the initial architecture slice."""

    def __init__(self, renderer, items, title="Menu") -> None:
        self.renderer = renderer
        self.items = items
        self.title = title
        self.index = 0

    def move_down(self) -> None:
        if self.items:
            self.index = (self.index + 1) % len(self.items)

    def move_up(self) -> None:
        if self.items:
            self.index = (self.index - 1) % len(self.items)

    def selected(self):
        if not self.items:
            return None
        return self.items[self.index]

    def render(self) -> None:
        self.renderer.draw_centered_text(self.title, 0)
        for position, item in enumerate(self.items):
            prefix = "> " if position == self.index else "  "
            self.renderer.draw_text(prefix + item, 8, 14 + position * 10)