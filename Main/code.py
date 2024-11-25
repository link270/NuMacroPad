import board, busio, time

from kmk.modules.holdtap import HoldTap
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.extensions.display.ssd1306 import SSD1306

# Define Pins

pixel_pin = board.D10
scl_pin = board.A3
sda_pin = board.A2
col_pins = (board.D6, board.D7, board.D8, board.D9)
row_pins = (board.D0, board.D1, board.D2,
            board.D3, board.D4, board.D5)


# KEYBOARD SETUP

keyboard = KMKKeyboard()

keyboard.col_pins = col_pins
keyboard.row_pins = row_pins
keyboard.diode_orientation = DiodeOrientation.COL2ROW


# RGB SETUP

rgb = RGB(pixel_pin=pixel_pin, num_pixels=19,
        hue_default=172, sat_default=255, val_default=128,
        animation_speed=1, breathe_center=2,
        animation_mode=AnimationModes.BREATHING_RAINBOW
        )

keyboard.extensions.append(rgb)


# DISPLAY SETUP

i2c = busio.I2C(scl_pin, sda_pin)

display_bus = SSD1306(i2c, device_address=0x3c)

display = Display(
#     # Mandatory:
    display=display_bus,
#     # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=1.0, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)

display.entries = [
    ImageEntry(image="LG_Triforce.bmp", x=0, y=0),
    TextEntry(text="NuMacroPad", x=0, y=0),
    TextEntry(text="By: Link270", x=0, y=12),
]

keyboard.extensions.append(display)


# Setup HoldTap

holdtap = HoldTap()
# optional: set a custom tap timeout in ms
# holdtap.tap_time = 300
keyboard.modules.append(holdtap)


# Custom Key Setup

class LimitKey():
    def __init__(self):
        print("init Limit Key")

    def on_press(self, keyboard, coord_int=None):
        if rgb.animation_mode==AnimationModes.BREATHING_RAINBOW:
           rgb.animation_mode=AnimationModes.STATIC
           print("Setting to Static")
        else:
           rgb.animation_mode=AnimationModes.BREATHING_RAINBOW
           print("Setting to Rainbow")

    def on_release(self, keyboard, coord_int=None):
        rgb.set_rgb_fill((0,255,0))
        rgb.show()

KC_A10 = LimitKey()

def DisplayTextToMiddle(text):
    display.entries = [
        TextEntry(text=text,x=64, y=16,
                  x_anchor="M", y_anchor="M"),]

    display.render(0)

class CustomReset():
    def __init__(self):
        print("init Custom Reset")

    def on_press(self, keyboard, coord_int=None):
        rgb.animation_mode=AnimationModes.STATIC
        rgb.set_rgb_fill((255,0,0))
        rgb.show()

    def on_release(self, keyboard, coord_int=None):
        rgb.set_rgb_fill((255,0,0))
        rgb.show()

        DisplayTextToMiddle("Re..................")
        time.sleep(0.1)

        DisplayTextToMiddle("Rest................")
        time.sleep(0.1)

        DisplayTextToMiddle("Restar..............")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarti............")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarting..........")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarting K........")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarting Key......")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarting Keybo....")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarting Keyboar..")
        time.sleep(0.1)

        DisplayTextToMiddle("Restarting Keyboard!")
        time.sleep(0.5)

        keyboard.add_key(KC.RESET)

KC_CUSTOMRESET = CustomReset()
HT_CustomReset = KC.HT(KC.B, KC_CUSTOMRESET)


# KEYMAP SETUP

keyboard.keymap = [
    [
        KC_A10, HT_CustomReset, KC.NO, KC.NO,
        KC.NUMLOCK, KC.KP_SLASH, KC.KP_ASTERISK, KC.KP_MINUS,
        KC.KP_7, KC.KP_8, KC.KP_9, KC.KP_PLUS,
        KC.KP_4, KC.KP_5, KC.KP_6, KC.NO,
        KC.KP_1, KC.KP_2, KC.KP_3, KC.KP_ENTER,
        KC.KP_0, KC.NO, KC.KP_DOT, KC.NO,
    ]
]


if __name__ == "__main__":
    keyboard.go() # type: ignore