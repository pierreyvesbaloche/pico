"""
This example script shows how to read button state with
debouncing that does not rely on time.sleep().
"""

from adafruit_hid.keycode import Keycode
from pimoroni.keybow import KeybowBoard, KeybowBoardConfiguration
from pimoroni.colors import Colors

def left_key(kbd):
    kbd.send(Keycode.COMMAND, Keycode.TAB)

def mid_key(kbd):
    kbd.send(Keycode.KEYPAD_ONE)

def right_key(kbd):
    kbd.send(Keycode.KEYPAD_TWO)

# Due to positioning of the keyboard, one might need to change the color layout
keybow = KeybowBoard(KeybowBoardConfiguration.MINI_CONFIG,
                        [Colors.RED, Colors.WHITE, Colors.BLUE], 
                        [left_key, mid_key, right_key])

while True:
    keybow.update()
