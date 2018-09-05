from ws2812 import WS2812
from BLE import BLE
from led_control import Control
from utilities import increment_color_all, decrement_color_all
from network import Bluetooth
import time


NUM_OF_LEDS = 100

#Initiate LED control
chain = WS2812(ledNumber=NUM_OF_LEDS, intensity=1)
led_control = Control(chain, NUM_OF_LEDS, initial_state = (0,0,0))
led_control.start()

#flash red
increment_color_all(led_control, "red", 0, 20)
decrement_color_all(led_control, "red", 20, 0)

#Initiate Bluetooth and start scanning for devices
ble = BLE(led_control)
ble.start_scan()

#flash green
increment_color_all(led_control, "green", 0, 20)
decrement_color_all(led_control, "green", 20, 0)
