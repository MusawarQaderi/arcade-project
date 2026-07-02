"""Input handling for joysticks and buttons."""


class InputManager:
    """Normalizes raw hardware input into a small, stable API."""

    def __init__(self, hardware) -> None:
        self.hardware = hardware
        self.current = self._empty_snapshot()
        self.previous = self._empty_snapshot()

    def update(self):
        self.previous = self.current
        self.current = self.hardware.input.read()
        return self.current

    def pressed(self, player: str, control: str) -> bool:
        return bool(self.current[player][control])

    def just_pressed(self, player: str, control: str) -> bool:
        return bool(self.current[player][control]) and not bool(self.previous[player][control])

    def _empty_snapshot(self):
        return {
            "player1": {"x": 0, "y": 0, "button": False},
            "player2": {"x": 0, "y": 0, "button": False},
        }