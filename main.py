from ws2812 import WS2812
import machine
from MQTT import MQTT
from led_control import Control
from WiFi import WiFi
from network_config import mqtt_config
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

#Initialize MQTT
mqtt = MQTT(led_control, "Moonmoon",
                mqtt_config['address'],
                mqtt_config['port'],
                mqtt_config['username'],
                mqtt_config['user_key'],
                mqtt_config['topic'])
#Initialize WiFi and start scanning for networks
wifi = WiFi(mqtt)

print ("Ready")

#flash green
increment_color_all(led_control, "green", 0, 20)
decrement_color_all(led_control, "green", 20, 0)
