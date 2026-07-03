"""Entry point for the Pico 2W arcade console.

Copy this file together with config.py, hardware.py, renderer.py, storage.py,
and the engine/ui/games folders to the Pico filesystem root.
"""

# MicroPython/Thonny can run main.py from a subfolder while the current working
# directory stays at /. Add the script folder to sys.path so sibling imports such
# as config.py are still found.
try:
    import sys

    _file = globals().get("__file__", "")
    _here = _file.rsplit("/", 1)[0] if "/" in _file else ""
    if _here and _here not in sys.path:
        sys.path.append(_here)
except Exception:
    pass

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
