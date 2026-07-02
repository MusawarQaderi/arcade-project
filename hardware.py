"""Hardware abstraction for the Pico arcade console."""

from config import Config

try:
    from machine import ADC, I2C, Pin
    import ssd1306
except ImportError:
    ADC = None
    I2C = None
    Pin = None
    ssd1306 = None


class NullDisplay:
    """Fallback display used outside MicroPython."""

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

    def show(self) -> None:
        return None


class NullInput:
    """Fallback input device used outside MicroPython."""

    def read(self):
        return {
            "player1": {"x": 0, "y": 0, "button": False},
            "player2": {"x": 0, "y": 0, "button": False},
        }


class Hardware:
    """Owns the display and will later own the input devices."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.display = self._create_display()
        self.input = self._create_input()

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
            return NullInput()

        return InputDevice(self.config)


class InputDevice:
    """Reads the two joysticks and two buttons."""

    def __init__(self, config: Config) -> None:
        self.player1_x = ADC(Pin(config.player1_x_pin))
        self.player1_y = ADC(Pin(config.player1_y_pin))
        self.player1_button = Pin(config.player1_button_pin, Pin.IN, Pin.PULL_UP)
        self.player2_x = ADC(Pin(config.player2_x_pin))
        self.player2_y = ADC(Pin(config.player2_y_pin))
        self.player2_button = Pin(config.player2_button_pin, Pin.IN, Pin.PULL_UP)

    def read(self):
        return {
            "player1": {
                "x": self.player1_x.read_u16(),
                "y": self.player1_y.read_u16(),
                "button": self.player1_button.value() == 0,
            },
            "player2": {
                "x": self.player2_x.read_u16(),
                "y": self.player2_y.read_u16(),
                "button": self.player2_button.value() == 0,
            },
        }