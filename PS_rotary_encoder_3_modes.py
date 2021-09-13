import rotaryio
import time
import board
import digitalio

import neopixel
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

from adafruit_hid.mouse import Mouse

# setup neopixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1, auto_write=False)

# setup encoder
encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)
last_position = 0
current_position = 0
position_change = 0
movement = False
increment = 0

# setup mode button
MODE_BUTTON = digitalio.DigitalInOut(board.D12)
MODE_BUTTON.direction = digitalio.Direction.INPUT
MODE_BUTTON.pull = digitalio.Pull.UP

mode_counter = 0  # define delay to smooth the buttons
debounce_time = 0.2

# color table for the neopixel (red, green, blue) 0-255
# modes 1-6
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (180, 0, 255)

# you must add colors to this array if you add more modes
mode_color = [RED, YELLOW, GREEN, BLUE]

MODE_BUTTON_state = None
key_pressed = False


def direction_change():
    global last_position
    global increment
    global position_change
    global current_position
    current_position = encoder.position
    position_change = current_position - last_position

    if current_position > last_position:
        movement = True
        increment = 1
        # print(increment)

    elif current_position < last_position:
        movement = False
        increment = -1
        # print(increment)
    else:
        increment = 0

    return position_change, increment


def mode_button_check():
    global mode_counter
    # Check the mode button
    if not MODE_BUTTON.value:
        mode_counter += 1
        # print(mode_counter)
        time.sleep(debounce_time)  # debounce delay

        if mode_counter > 3:
            mode_counter = 0

    return mode_counter


def make_it_a_mouse(increment):
    m = Mouse(usb_hid.devices)
    m.move(wheel=increment)

def make_it_a_mouse_click(increment):
    m = Mouse(usb_hid.devices)
    # Move the mouse while holding down the left button. (click-drag).
    m.press(Mouse.LEFT_BUTTON)
    m.move(x=5*(increment), y=0)
    m.release_all()

def zoom_in_out(increment):

    # make it a keyboard first
    kbd = Keyboard(usb_hid.devices)
    kbdLayout = KeyboardLayoutUS(kbd)
    kbd.press(Keycode.ALT)

    make_it_a_mouse(increment)

    # make it a keyboard again
    kbd = Keyboard(usb_hid.devices)
    kbdLayout = KeyboardLayoutUS(kbd)
    kbd.release_all()


def scroll_in_out(increment):
    make_it_a_mouse(increment)

def rotate(increment):

    # make it a keyboard first
    kbd = Keyboard(usb_hid.devices)
    kbdLayout = KeyboardLayoutUS(kbd)
    kbd.press(Keycode.R,)

    make_it_a_mouse_click(increment)

    # make it a keyboard again
    kbd = Keyboard(usb_hid.devices)
    kbdLayout = KeyboardLayoutUS(kbd)
    kbd.release_all()



while True:
    direction_change()
# zoom
    if position_change > 0  and mode_counter == 0:
        for _ in range(position_change):
            zoom_in_out(increment)
    elif position_change < 0 and mode_counter == 0:
        for _ in range(-position_change):
            zoom_in_out(increment)
# scroll
    if position_change > 0  and mode_counter == 1:
        for _ in range(position_change):
            scroll_in_out(increment)
    elif position_change < 0 and mode_counter == 1:
        for _ in range(-position_change):
            scroll_in_out(increment)
# rotate
    if position_change > 0  and mode_counter == 2:
        for _ in range(position_change):
            rotate(position_change)
    elif position_change < 0 and mode_counter == 2:
        for _ in range(-position_change):
            rotate(position_change)
# brush size TODO

    mode_button_check()

    pixels.fill(mode_color[mode_counter])
    pixels.show()

    last_position = current_position
