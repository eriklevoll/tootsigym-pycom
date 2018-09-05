from ws2812 import WS2812
from BLE import BLE
from led_control import Control
from utilities import increment_color_all, decrement_color_all

# NUM_OF_LEDS = 100
#
# #Initiate LED control
# chain = WS2812(ledNumber=NUM_OF_LEDS, intensity=1)
# led_control = Control(chain, NUM_OF_LEDS, initial_state = (0,0,0))
# led_control.start()
#
# #flash red
#increment_color_all(led_control, "red", 0, 20)
#decrement_color_all(led_control, "red", 20, 0)

#Initiate Bluetooth and start scanning for devices
#bluetooth = BLE(led_control)
#bluetooth.scan(True)
#
# bluetooth2 = BLE(led_control)
# bluetooth2.scan(True)

#flash green
#increment_color_all(led_control, "green", 0, 20)
#decrement_color_all(led_control, "green", 20, 0)

def connection_callback(bt_o):
    """
    Callback function for bluetooth connection triggers (connected/disconnected)
    """
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Device connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Device disconnected")

def characteristic_callback(characteristic):
    print ('Bluetooth.CHAR_NOTIFY_EVENT')
    val = characteristic.value().decode('utf-8')
    print (val)
    if ("disconnect" in val):
        v2 = val.split(":::")[1]
        print (v2, device_names)
        conn = device_names[v2]
        conn.disconnect()
        del device_names[v2]
    else:
        characteristic.write(b'response')

from network import Bluetooth
import time
bt = Bluetooth()
bt.start_scan(-1)

bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=connection_callback)

conn_mc = 0

device_names = {}

print ("Start")
while True:
    adv = bt.get_adv()
    if not adv:
        time.sleep(1)
        continue

    device_name = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
    if adv and "MB_APP" in device_name:
        #try:
        id = device_name.split(":::")[1]
        if (id in device_names):
            print ("juba on", id, device_names)
            continue
        print (id, device_names)
        print ("Connecting")
        conn = bt.connect(adv.mac)
        device_names[id] = conn
        time.sleep(1)
        services = conn.services()
        for service in services:
            time.sleep(0.050)
            if type(service.uuid()) == bytes:
                print('Reading chars from service = {}'.format(service.uuid()))
            else:
                print('Reading chars from service = %x' % service.uuid())
            chars = service.characteristics()
            for char in chars:
                if (char.properties() & Bluetooth.PROP_READ):
                    print('char {} value = {}'.format(char.uuid(), char.read()))
                    val = char.read().decode('utf-8')
                    if (val == id):
                        char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=characteristic_callback)
                        char.write(b'CONN_OK')
                    print ("val:", val, val == id)

        #conn.disconnect()
        print ("Started scanning again")
        bt.start_scan(-1)
        time.sleep(1)
        print (bt.isscanning())
        #except:
            #pass
    else:
        time.sleep(1)
