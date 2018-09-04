from ws2812 import WS2812
from BLE import BLE
from led_control import Control
from utilities import increment_color_all, decrement_color_all
import time

NUM_OF_LEDS = 100

#Initiate LED control
chain = WS2812(ledNumber=NUM_OF_LEDS, intensity=1)
led_control = Control(chain, NUM_OF_LEDS, initial_state = (0,0,0))
led_control.start()

#flash red
increment_color_all(led_control, "red", 0, 20)
decrement_color_all(led_control, "red", 20, 0)

#Initiate and set up Bluetooth with 1 service and 3 characteristics
bluetooth = BLE(led_control, device_name='Märdi muunbord', service_uuid='12EFFA29-0B6E-40B3-9181-BE9509B23200')
bluetooth.add_service('4880c12cfdcb40778920a450d7f9b907', characters=3)
bluetooth.add_read_characteristic('fdc26ec4-6d71-4442-9f81-55bc21d658d6')
bluetooth.add_write_characteristic('afc13ec4-6d71-4442-9f81-55bc21d658d6')
bluetooth.add_indicate_characteristic('afcafec4-6d71-4442-9f81-55bc21d658d6')
bluetooth.advertise(True)

#flash green
increment_color_all(led_control, "green", 0, 20)
decrement_color_all(led_control, "green", 20, 0)