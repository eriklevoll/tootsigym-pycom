from MQTT import MQTT
from WiFi import WiFi
from led_control import Control
from utilities import increment_color_all, decrement_color_all

print ("Initiating...")

#Initiate LED control
led_control = Control(num_of_leds = 198, initial_state = (0,30,30))

#Initialize MQTT
mqtt = MQTT(led_control, device_name = "moon_pycom")
#Initialize WiFi and start scanning for networks
wifi = WiFi(mqtt)
