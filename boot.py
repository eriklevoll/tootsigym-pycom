import pycom
from network import Bluetooth

bluetooth = Bluetooth()
bluetooth.deinit()

pycom.heartbeat(False)
pycom.rgbled(0x000014)
