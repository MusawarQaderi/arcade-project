"""Central configuration for the Pico 2W arcade console."""


class Config:
    """Project-wide constants and MicroPython-safe tunables."""

    APP_NAME = "Arcade Console"
    WIDTH = 128
    HEIGHT = 64
    FPS = 30

    # SSD1306 I2C pins are intentionally kept compatible with the existing repo.
    I2C_SCL_PIN = 1
    I2C_SDA_PIN = 0
    OLED_I2C_ADDR = 0x3C

    # Required one-axis joystick mapping:
    # Joystick 1: VRy -> GP26 / ADC0, SW -> GP14 with PULL_UP
    # Joystick 2: VRy -> GP27 / ADC1, SW -> GP15 with PULL_UP
    PLAYER1_AXIS_PIN = 26
    PLAYER1_BUTTON_PIN = 14
    PLAYER2_AXIS_PIN = 27
    PLAYER2_BUTTON_PIN = 15

    # Set these to True if an installed joystick feels inverted.
    PLAYER1_AXIS_INVERT = False
    PLAYER2_AXIS_INVERT = False

    # Input behavior. Values are conservative for cheap joystick modules.
    CALIBRATION_SAMPLES = 32
    CALIBRATION_SAMPLE_DELAY_MS = 4
    AXIS_DEADZONE_ENTER = 9000
    AXIS_DEADZONE_EXIT = 5500
    BUTTON_DEBOUNCE_MS = 35
    BUTTON_BACK_HOLD_MS = 650
    MENU_REPEAT_DELAY_MS = 330
    MENU_REPEAT_MS = 120

    # OLED rendering. SSD1306 text is 8 px high; keep all UI rows aligned.
    FONT_WIDTH = 8
    FONT_HEIGHT = 8
    ROWS = 8
    COLS = 16
    STORAGE_FILE = "save/state.json"

    def __init__(self) -> None:
        self.app_name = self.APP_NAME
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.fps = self.FPS
        self.i2c_scl_pin = self.I2C_SCL_PIN
        self.i2c_sda_pin = self.I2C_SDA_PIN
        self.oled_i2c_addr = self.OLED_I2C_ADDR
        self.player1_axis_pin = self.PLAYER1_AXIS_PIN
        self.player1_button_pin = self.PLAYER1_BUTTON_PIN
        self.player2_axis_pin = self.PLAYER2_AXIS_PIN
        self.player2_button_pin = self.PLAYER2_BUTTON_PIN
        self.player1_axis_invert = self.PLAYER1_AXIS_INVERT
        self.player2_axis_invert = self.PLAYER2_AXIS_INVERT
        self.calibration_samples = self.CALIBRATION_SAMPLES
        self.calibration_sample_delay_ms = self.CALIBRATION_SAMPLE_DELAY_MS
        self.axis_deadzone_enter = self.AXIS_DEADZONE_ENTER
        self.axis_deadzone_exit = self.AXIS_DEADZONE_EXIT
        self.button_debounce_ms = self.BUTTON_DEBOUNCE_MS
        self.button_back_hold_ms = self.BUTTON_BACK_HOLD_MS
        self.menu_repeat_delay_ms = self.MENU_REPEAT_DELAY_MS
        self.menu_repeat_ms = self.MENU_REPEAT_MS
        self.font_width = self.FONT_WIDTH
        self.font_height = self.FONT_HEIGHT
        self.rows = self.ROWS
        self.cols = self.COLS
        self.storage_file = self.STORAGE_FILE
