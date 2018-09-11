import pycom
from network import WLAN

pycom.heartbeat(False)
#pycom.rgbled(0x0000ff)
wlan = WLAN() #close wlan
wlan.deinit()
