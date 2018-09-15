import pycom
from network import WLAN

pycom.heartbeat(False)
pycom.rgbled(0x001400)
wlan = WLAN() #close wlan
wlan.deinit()
