import pycom
from network import WLAN

pycom.heartbeat(False)
wlan = WLAN() #close wlan
wlan.deinit()
