from ws2812 import WS2812
import machine
from MQTT import MQTT
from led_control import Control
from utilities import increment_color_all, decrement_color_all

print ("Initiating...")

NUM_OF_LEDS = 198

#Initiate LED control
chain = WS2812(ledNumber=NUM_OF_LEDS, intensity=1)
led_control = Control(chain, NUM_OF_LEDS, initial_state = (0,0,0))
led_control.start()

#flash red
increment_color_all(led_control, "red", 0, 20)
decrement_color_all(led_control, "red", 20, 0)

NETWORK_NAME        = "Tehnolabor"
NETWORK_KEY         = "009E00B7C9"
NETWORK_SECURITY    = 4

wlan = WLAN(mode=WLAN.STA)
wlan.connect(NETWORK_NAME, auth=(NETWORK_SECURITY, NETWORK_KEY), timeout= 5000)

while not wlan.isconnected():
    machine.idle()

print ("Connected to WiFi\n")

#Initiate MQTT and start listening for messages
mqtt = MQTT(led_control, "Moonmoon", "m20.cloudmqtt.com", 11957, "ayogkqnq", "_e4HiuI73ywB", "moon")

print ("Ready")

#flash green
increment_color_all(led_control, "green", 0, 20)
decrement_color_all(led_control, "green", 20, 0)
