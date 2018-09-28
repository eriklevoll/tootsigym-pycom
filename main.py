from MQTT import MQTT
from WiFi import WiFi
from led_control import Control

print ("Initiating...")

#Initiate LED control
led_control = Control(num_of_leds = 198, initial_state = (0,0,0))

#Initialize MQTT
mqtt = MQTT(led_control, device_name = "moon_pycom")
#Initialize WiFi and start scanning for networks
wifi = WiFi(mqtt)
