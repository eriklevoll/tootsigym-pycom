import pycom
from network import Bluetooth
​
#Turn off bluetooth adapter
bluetooth = Bluetooth()
bluetooth.deinit()

pycom.heartbeat(False)
pycom.rgbled(0x000014)
