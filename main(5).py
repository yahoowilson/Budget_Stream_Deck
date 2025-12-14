import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display
from kmk.extensions.display.ssd1306 import SSD1306

# -----------------------------
# Keyboard init
# -----------------------------
keyboard = KMKKeyboard()

# -----------------------------
# Matrix pins (from your schematic)
# -----------------------------
keyboard.row_pins = (
    board.GP26,  # ROW0
    board.GP27,  # ROW1
    board.GP28,  # ROW2
)

keyboard.col_pins = (
    board.GP2,   # COL0
    board.GP1,   # COL1
    board.GP3,   # COL2
)

keyboard.diode_orientation = keyboard.DIODE_COL2ROW

# -----------------------------
# Rotary Encoder
# -----------------------------
encoder = EncoderHandler()
encoder.pins = (
    (board.GP0, board.GP1),  # ENC_A, ENC_B
)
encoder.map = (
    (KC.VOLU, KC.VOLD),
)
keyboard.modules.append(encoder)

# -----------------------------
# OLED Display (SSD1306)
# -----------------------------
i2c = busio.I2C(
    board.GP7,  # SCL
    board.GP6,  # SDA
)

display = Display(
    display=SSD1306(
        i2c=i2c,
        width=128,
        height=64,
        device_address=0x3C,
    ),
    brightness=1,
)

keyboard.extensions.append(display)

# -----------------------------
# Keymap (3x3 matrix, one unused)
# -----------------------------
keyboard.keymap = [
    [
        KC.MUTE,              KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK,
        KC.MEDIA_PREV_TRACK,  KC.LCTL(KC.C),        KC.LCTL(KC.V),
        KC.LALT(KC.TAB),      KC.ESC,               KC.NO,
    ]
]

# -----------------------------
# OLED content
# -----------------------------
def oled_task():
    display.clear()
    display.text("Budget Stream Deck", 0, 0, 1)
    display.text("Layer: 0", 0, 16, 1)
    display.text("Encoder = Volume", 0, 32, 1)
    display.show()

keyboard.after_matrix_scan = oled_task

# -----------------------------
# Start KMK
# -----------------------------
if __name__ == "__main__":
    keyboard.go()
