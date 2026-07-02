"""Central configuration for the arcade console."""


class Config:
    """Project-wide constants and tunables."""

    APP_NAME = "Arcade Console"
    WIDTH = 128
    HEIGHT = 64
    FPS = 30
    I2C_SCL_PIN = 1
    I2C_SDA_PIN = 0
    OLED_I2C_ADDR = 0x3C
    PLAYER1_X_PIN = 26
    PLAYER1_Y_PIN = 27
    PLAYER1_BUTTON_PIN = 14
    PLAYER2_X_PIN = 28
    PLAYER2_Y_PIN = 29
    PLAYER2_BUTTON_PIN = 15
    STORAGE_FILE = "save/state.json"

    def __init__(self) -> None:
        self.app_name = self.APP_NAME
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.fps = self.FPS
        self.i2c_scl_pin = self.I2C_SCL_PIN
        self.i2c_sda_pin = self.I2C_SDA_PIN
        self.oled_i2c_addr = self.OLED_I2C_ADDR
        self.player1_x_pin = self.PLAYER1_X_PIN
        self.player1_y_pin = self.PLAYER1_Y_PIN
        self.player1_button_pin = self.PLAYER1_BUTTON_PIN
        self.player2_x_pin = self.PLAYER2_X_PIN
        self.player2_y_pin = self.PLAYER2_Y_PIN
        self.player2_button_pin = self.PLAYER2_BUTTON_PIN
        self.storage_file = self.STORAGE_FILE