"""Persistent storage for settings and statistics."""

try:
    import ujson as json
except ImportError:
    import json

from config import Config


class Storage:
    """Loads and saves arcade state as JSON."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.state = {
            "settings": {
                "brightness": 1,
                "difficulty": 1,
                "sound": True,
            },
            "stats": {
                "play_time": 0,
                "games_started": 0,
                "games_finished": 0,
                "wins": 0,
                "losses": 0,
            },
            "highscores": {},
            "achievements": [],
        }

    def _ensure_defaults(self) -> dict:
        settings = self.state.setdefault("settings", {})
        settings.setdefault("brightness", 1)
        settings.setdefault("difficulty", 1)
        settings.setdefault("sound", True)

        stats = self.state.setdefault("stats", {})
        stats.setdefault("play_time", 0)
        stats.setdefault("games_started", 0)
        stats.setdefault("games_finished", 0)
        stats.setdefault("wins", 0)
        stats.setdefault("losses", 0)

        self.state.setdefault("highscores", {})
        self.state.setdefault("achievements", [])
        return self.state

    def load(self) -> dict:
        try:
            with open(self.config.storage_file, "r") as handle:
                loaded = json.load(handle)
        except OSError:
            return self.state

        if isinstance(loaded, dict):
            self.state.update(loaded)
        return self._ensure_defaults()

    def save(self) -> None:
        try:
            with open(self.config.storage_file, "w") as handle:
                json.dump(self.state, handle)
        except OSError:
            pass

    def get_setting(self, key, default=None):
        return self.state.setdefault("settings", {}).get(key, default)

    def set_setting(self, key, value) -> None:
        self.state.setdefault("settings", {})[key] = value

    def toggle_setting(self, key) -> None:
        current = bool(self.get_setting(key, False))
        self.set_setting(key, not current)

    def cycle_setting(self, key, values) -> None:
        if not values:
            return

        current = self.get_setting(key, values[0])
        try:
            index = values.index(current)
        except ValueError:
            index = 0
        self.set_setting(key, values[(index + 1) % len(values)])

    def reset_highscores(self) -> None:
        self.state["highscores"] = {}

    def get_highscore(self, game_name) -> int:
        return int(self.state.setdefault("highscores", {}).get(game_name, 0))

    def set_highscore(self, game_name, score: int) -> None:
        highscores = self.state.setdefault("highscores", {})
        current = int(highscores.get(game_name, 0))
        if score > current:
            highscores[game_name] = int(score)

    def record_game_started(self) -> None:
        self.state.setdefault("stats", {})["games_started"] = self.state["stats"].get("games_started", 0) + 1

    def record_game_finished(self) -> None:
        self.state.setdefault("stats", {})["games_finished"] = self.state["stats"].get("games_finished", 0) + 1
