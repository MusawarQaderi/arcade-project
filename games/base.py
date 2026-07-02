"""Base game interface for arcade titles."""


class GameBase:
    """Minimal game contract used by the engine."""

    name = "Game"

    def reset(self) -> None:
        raise NotImplementedError

    def update(self, input_manager) -> None:
        raise NotImplementedError

    def render(self, renderer) -> None:
        raise NotImplementedError

    def get_score(self) -> int:
        return 0