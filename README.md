# WS2812 neopixel pycom mqtt controller

## Project structure:
```
/lib
    MQTT.py           - main mqtt object for all data transfer handling
    umqtt.py          - Message Queuing Telemetry Transport base class
    WiFi.py           - WiFi network class to manage scanning and connecting
    network_config.py - Wifi and mqtt connection configurations
    led_control.py    - LED object to control color values
    utilities.py      - General useful functions
    ws2812.py         - Neopixel WS2812 control library
/boot.py              - This file is launched first when device is powered on
/main.py              - Launched after boot.py. Main program code goes here
```
