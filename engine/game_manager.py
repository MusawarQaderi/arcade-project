"""Game registry and launch control."""


class GameManager:
    """Stores available games and tracks the active selection."""

    def __init__(self) -> None:
        self.games = {}

    def register(self, name, game) -> None:
        self.games[name] = game

    def get(self, name):
        return self.games.get(name)

    def names(self):
        return list(self.games.keys())

    def current(self):
        if not self.games:
            return None
        first_name = self.names()[0]
        return self.games[first_name]