"""Entry point for the arcade console."""

from config import Config
from engine.core import ArcadeApp
from hardware import Hardware
from renderer import Renderer
from storage import Storage


def main() -> None:
    config = Config()
    hardware = Hardware(config)
    renderer = Renderer(hardware.display, config)
    storage = Storage(config)
    app = ArcadeApp(config=config, hardware=hardware, renderer=renderer, storage=storage)
    app.run()


if __name__ == "__main__":
    main()