# WS2812 neopixel pycom bluetooth controller

## Project structure:
```
/lib
    BLE.py          - Class for managing bluetooth connection
    led_control.py  - LED object to control color values
    utilities.py    - General useful functions
    ws2812.py       - Neopixel WS2812 control library
/boot.py            - This file is launched first when device is powered on
/main.py            - Launched after boot.py. Main program code goes here
```
