"""Hardware abstraction for Raspberry Pi Pico 2W + SSD1306 + 2 one-axis joysticks."""

from config import Config

try:
    from machine import ADC, I2C, Pin
except ImportError:
    ADC = None
    I2C = None
    Pin = None

try:
    import ssd1306
except ImportError:
    ssd1306 = None


class NullDisplay:
    """Fallback display used when running syntax checks outside MicroPython."""

    width = 128
    height = 64

    def fill(self, value: int) -> None:
        _ = value

    def text(self, text: str, x: int, y: int, color: int = 1) -> None:
        _ = (text, x, y, color)

    def pixel(self, x: int, y: int, color: int = 1) -> None:
        _ = (x, y, color)

    def line(self, x1: int, y1: int, x2: int, y2: int, color: int = 1) -> None:
        _ = (x1, y1, x2, y2, color)

    def rect(self, x: int, y: int, width: int, height: int, color: int = 1) -> None:
        _ = (x, y, width, height, color)

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int = 1) -> None:
        _ = (x, y, width, height, color)

    def show(self) -> None:
        return None


class NullRawInput:
    """Fallback input source for desktop checks."""

    def read(self):
        return {
            "p1": {"axis": 32768, "button": False},
            "p2": {"axis": 32768, "button": False},
        }


class Hardware:
    """Owns raw hardware resources; higher-level input lives in engine.input."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.display = self._create_display()
        self.raw_input = self._create_input()

    def _create_display(self):
        if I2C is None or Pin is None or ssd1306 is None:
            return NullDisplay()

        i2c = I2C(
            0,
            scl=Pin(self.config.i2c_scl_pin),
            sda=Pin(self.config.i2c_sda_pin),
            freq=400000,
        )
        return ssd1306.SSD1306_I2C(
            self.config.width,
            self.config.height,
            i2c,
            addr=self.config.oled_i2c_addr,
        )

    def _create_input(self):
        if ADC is None or Pin is None:
            return NullRawInput()
        return RawInputDevice(self.config)


class RawInputDevice:
    """Reads only the required VRy analog axis and active-low button per player."""

    def __init__(self, config: Config) -> None:
        # Hardware mapping required by the Pico 2W build:
        # P1 VRy -> GP26/ADC0, P1 SW -> GP14/PULL_UP
        # P2 VRy -> GP27/ADC1, P2 SW -> GP15/PULL_UP
        self.player1_axis = ADC(Pin(config.player1_axis_pin))
        self.player1_button = Pin(config.player1_button_pin, Pin.IN, Pin.PULL_UP)
        self.player2_axis = ADC(Pin(config.player2_axis_pin))
        self.player2_button = Pin(config.player2_button_pin, Pin.IN, Pin.PULL_UP)

    def read(self):
        return {
            "p1": {
                "axis": self.player1_axis.read_u16(),
                "button": self.player1_button.value() == 0,
            },
            "p2": {
                "axis": self.player2_axis.read_u16(),
                "button": self.player2_button.value() == 0,
            },
        }
