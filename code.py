import rotaryio
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

from adafruit_hid.mouse import Mouse

button = digitalio.DigitalInOut(board.D12)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)

button_state = None
last_position = encoder.position
key_pressed = False

def make_it_a_mouse(increment):
    m = Mouse(usb_hid.devices)
    print(increment)
    m.move(wheel = increment)

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


while True:
    current_position = encoder.position
    position_change = current_position - last_position

    if (position_change > 0) and (key_pressed == True) :
        for _ in range(position_change):
            zoom_in_out(1)
            print(current_position)
    elif (position_change < 0) and (key_pressed == True) :
        for _ in range(-position_change):
            zoom_in_out(-1)
            print(current_position)
    last_position = current_position

    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        key_pressed = True
        button_state = None
