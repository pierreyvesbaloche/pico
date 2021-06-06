"""
Main Pimoroni Keybow Helper classes.
"""
from pimoroni.colors import Colors

import board
import usb_hid

import adafruit_dotstar

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from digitalio import DigitalInOut, Direction, Pull

class KeybowBoardConfiguration(object):
    MINI_CONFIG = 3
    STANDARD_CONFIG = 12

    # Mapping of Keybow Mini (3 Keys) GPIOs matching Red Robotics Pico 2 Pi Adaptor Board
    KEYBOM_MINI_GPIOS = [board.GP7, board.GP9, board.GP11]

    # Mapping of Keybow Standard (12 keys) GPIOs matching Red Robotics Pico 2 Pi Adaptor Board
    KEYBOM_STRD_GPIOS = [board.GP7, board.GP8, board.GP27, board.GP9,
                         board.GP26, board.GP10, board.GP11, board.GP18,
                         board.GP12, board.GP16, board.GP17, board.GP14]

class KeybowBoard(object):

    def __init__(self, configuration, colors, button_actions):
        if configuration not in (KeybowBoardConfiguration.MINI_CONFIG, KeybowBoardConfiguration.STANDARD_CONFIG):
            raise ValueError("Invalid Keybow configuration : should be either 3 or 12")
        # Save the Keybow type
        self.config = configuration

        # Define the keybow's HID Keyboard
        self.kbd = Keyboard(usb_hid.devices)

        # Define the keybow's pixels strip
        self.pixels = adafruit_dotstar.DotStar(board.GP2, board.GP3, self.config, brightness=0.1, auto_write=True)

        # Initialize the array of buttons
        self.btns = []

        # Retrieve the right configuration
        if self.config == KeybowBoardConfiguration.MINI_CONFIG:
            gpios = KeybowBoardConfiguration.KEYBOM_MINI_GPIOS
        else:
            gpios = KeybowBoardConfiguration.KEYBOM_STRD_GPIOS

        for i in range(len(button_actions)):
            self.btns.append(KeybowButton(gpios[i], i, self.pixels, colors[i], self.kbd, button_actions[i]))

    def update(self):
        for i in range(self.config):
            self.btns[i].check()

class KeybowButton(object):

    def __init__(self, board_pin, pixel_index, pixel_led, pixel_color, keyboard, key_function):
        self.pin = board_pin
        self.keyboard = keyboard
        self.btn = DigitalInOut(self.pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP
        self.previous_state = False
        self.pixel = pixel_led
        self.pixel_index = pixel_index
        self.color = pixel_color
        self.action = key_function
        print("New Button position:{} color:{} action:{}".format(pixel_index, str(pixel_color), str(key_function)))

    @property
    def index(self):
        return self.pixel_index

    @property
    def value(self):
        return self.btn.value

    @property
    def previous_state(self):
        return self.__previous_state

    @previous_state.setter
    def previous_state(self, state):
        self.__previous_state = state

    def check(self):
        cur_state = self.value
        if cur_state != self.previous_state:
            if not cur_state:
                print("Button {} is down".format(self.index))
                self.pixel[self.pixel_index] = Colors.BLACK
                self.action(self.keyboard)
            else:
                print("Button {} is up".format(self.index))
                self.pixel[self.pixel_index] = self.color
            self.previous_state = cur_state
