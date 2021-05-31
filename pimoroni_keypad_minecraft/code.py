# Adapted from Sandy J Macdonald's gist at https://gist.github.com/sandyjmacdonald/b465377dc11a8c83a8c40d1c9b990a90 
# Map a Pimoroni Pico Keypad to supply the Minecraft base commands

# Import Standard Libraries
import time
import board
import busio
import usb_hid

# Import Adafruit Libraries
import adafruit_dotstar
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Define the buttons' pixel
num_pixels = 16
pixels = adafruit_dotstar.DotStar(board.GP18, board.GP19, num_pixels, brightness=0.1, auto_write=True)

# Initiate the I2C settings
i2c = busio.I2C(board.GP5, board.GP4)
device = I2CDevice(i2c, 0x20)

# Define the keypad's Keyboard
kbd = Keyboard(usb_hid.devices)

# Define some colors
COLOR_RED = 0
COLOR_ORANGE = 1
COLOR_PEACH = 2
COLOR_YELLOW = 3
COLOR_YELLOW_GREEN = 4
COLOR_GREEN = 5
COLOR_GREEN_CYAN = 6
COLOR_CYAN = 7
COLOR_LIGHT_BLUE = 8
COLOR_BLUE = 9
COLOR_DARK_BLUE = 10
COLOR_BLUE_PURPLE = 11
COLOR_PURPLE = 12
COLOR_PURPLE_PINK = 13
COLOR_PINK = 14
COLOR_PINK_RED = 15

# Assign the custom colors to the keys : gree = navigation, yellow & peach = items, 
# cyan = jump, purple = crouch, pink = inventory, red = ESC
keys_colors = [COLOR_YELLOW, COLOR_RED, COLOR_GREEN, COLOR_PINK,
                COLOR_YELLOW, COLOR_GREEN, COLOR_GREEN, COLOR_GREEN,
                COLOR_YELLOW, COLOR_PEACH, COLOR_PEACH, COLOR_PURPLE,
                COLOR_YELLOW, COLOR_PEACH, COLOR_PEACH, COLOR_CYAN]

# Define if each keypress "shall say this only once" ;)
keys_repetition = [True, True, False, True,
                    True, False, False, False,
                    True, True, True, False,
                    True, True, True, False]

# Define the key codes to send
keys_function = [Keycode.KEYPAD_ONE, Keycode.ESCAPE, Keycode.Z, Keycode.E,
                    Keycode.KEYPAD_TWO, Keycode.Q, Keycode.S, Keycode.D,
                    Keycode.KEYPAD_THREE, Keycode.KEYPAD_FIVE, Keycode.KEYPAD_SIX, Keycode.LEFT_SHIFT,
                    Keycode.KEYPAD_FOUR, Keycode.KEYPAD_SEVEN, Keycode.KEYPAD_EIGHT, Keycode.SPACEBAR]

# Great color picking function : Thanks Sandy !
def colourwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

# Read all buttons states : Thanks Sandy !
def read_button_states(x, y):
    pressed = [0] * num_pixels
    with device:
        device.write(bytes([0x0]))
        result = bytearray(2)
        device.readinto(result)
        b = result[0] | result[1] << 8
        for i in range(x, y):
            if not (1 << i) & b:
                pressed[i] = 1
            else:
                pressed[i] = 0
    return pressed

# Manage the behavior of the keypad button, based on its position
def handle_button_state(index):
    global pressed
    global held
    global keys_colors
    global keys_repetition
    global keys_function
    if pressed[index]:
        pixels[index] = (0, 0, 0)
        if not held[index]:
            kbd.press(keys_function[index])
            if keys_repetition[index]:
                held[index] = 1
    else:
        pixels[index] = colourwheel(keys_colors[index] * num_pixels)
        held[index] = 0
        kbd.release(keys_function[index])

# Main endless loop
held = [0] * num_pixels
while True:
    pressed = read_button_states(0, num_pixels)
    for i in range(16):
        handle_button_state(i)
