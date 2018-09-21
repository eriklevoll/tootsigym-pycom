from MQTT import MQTT
from WiFi import WiFi
from led_control import Control
from utilities import increment_color_all, decrement_color_all

print ("Initiating...")

#Initiate LED control
led_control = Control(num_of_leds = 198, initial_state = (0,255,0))

#Initialize MQTT
mqtt = MQTT(led_control, device_name = "moon_pycom")
#Initialize WiFi and start scanning for networks
wifi = WiFi(mqtt)

print ("Ready")

#Slowly turn off leds
decrement_color_all(led_control, "green", 255, 0)
