# Pimoroni Keybow upgrade to Pico

# Description

This project turns a Pimoroni Pico Keybow ( <https://shop.pimoroni.com/products/keybow-mini-3-key-macro-pad-kit> ) into a Pico Powered Edition, thanks to Red Robotics Pico 2 Pi adaptor board ( <https://www.tindie.com/products/redrobotics/pico-2-pi-adapter-board/>).

Tested with Adafruit 6.3.0 CircuitPython library ( <https://circuitpython.org/board/raspberry_pi_pico/> )for the Raspberry Pi Pico ( <https://www.raspberrypi.org/documentation/rp2040/getting-started/> ).

# Setup

1. Download and install Adafruit's CircuitPython on your Raspberry Pico.
1. Once the board is reinitialised, create a `lib` folder at the root of the `CIRCUITPY` drive.
1. Download the associated libraries from <https://circuitpython.org/libraries> and extract locally the corresponding zip file.
1. From it, copy the following files & folder onto your `CIRCUITPY\lib`folder:
   - adafruit_dotstar.mpy
   - adafruit_hid
1. Copy this project's `code.py`file and `lib` folder to the root of your `CIRCUITPY` drive.

# Result

![](project.png)