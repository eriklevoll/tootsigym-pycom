from network import Bluetooth
from utilities import increment_color_all, decrement_color_all
from machine import Timer
import time
import binascii
import machine

class BLE:
    def __init__(self, led_control):
        """
        Constructor

        Args:
            led_control:   LED control object
        """
        self.led_control    = led_control
        self.bluetooth      = Bluetooth()
        self.devices_dict   = {}

        self.bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.NEW_ADV_EVENT, handler=self.connection_callback)

    def start_scan(self):
        """
        Starts BLE scan
        """
        self.bluetooth.start_scan(-1)

    def connection_callback(self, bt_o):
        """
        Callback function for bluetooth connection triggers (connected/disconnected)
        """
        events = bt_o.events()
        if  events & Bluetooth.CLIENT_CONNECTED:
            print("Device connected")
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            print("Device disconnected")
        elif events & Bluetooth.NEW_ADV_EVENT:
<<<<<<< HEAD
            #print ("Got something")
=======
>>>>>>> 6c8e37f9b883069f02d3db08f6a7547fa4a5ca6b
            self.parse_adv()

    def parse_adv(self):
        """
        Parse advertisement package data
        """
        adv = self.bluetooth.get_adv()
        if adv is None: return

        device_name = self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        if device_name is None: return

        if "MB_APP" in device_name:
            id = device_name.split(":::")[1]
            if (id in self.devices_dict): return

            print (id, self.devices_dict)
            print ("Connecting", adv.mac)

            conn = self.bluetooth.connect(adv.mac)
            self.devices_dict[id] = conn
            time.sleep(0.150)

            self.parse_services(conn.services(), id)

            print ("Started scanning again")
            self.bluetooth.start_scan(-1)
            time.sleep(0.050)

    def parse_services(self, services, id):
        """
        Loop through connection services
        """
        for service in services:
            time.sleep(0.050)
            self.parse_characteristics(service.characteristics(), id)

    def parse_characteristics(self, chars, id):
        """
        Loop through service characteristics
        """
        for char in chars:
            if (char.properties() & Bluetooth.PROP_READ):
                if (char.read().decode('utf-8') == id):
                    self.set_notify_listener(char)

    def set_notify_listener(self, char):
        """
        Set notify trigger on characteristic
        """
        try:
            char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)
            char.write(b'CONN_OK')
        except:
            print ("Failed to set trigger")

    def characteristic_callback(self, characteristic):
        """
        Callback function for GATT characteristic
        """
        print ('Bluetooth.CHAR_NOTIFY_EVENT')
        char_value = characteristic.value().decode('utf-8')
        print (char_value)
        if ("disconnect" in char_value):
            device_id = char_value.split(":::")[1]
            conn = self.devices_dict[device_id]
            conn.disconnect()
            del self.devices_dict[device_id]
        else:
            self.parse_char_data(char_value)

    def get_device_id(self, data):
        """
        Read device ID tag from device full name

        Args:
            data:   device name data stored in ADV_NAME_CMPL. Form: MB_APP:::00000000

            returns: device id
        """
        device_id = "0"
        if ":::" in data:
            device_id = data.split(":::")[1]
        return device_id

    def uuid2bytes(self, uuid):
        """
        Converts standard uuid format to little endian

        Credit @jmarcelino
        https://forum.pycom.io/topic/530/working-with-uuid/2
        """
        uuid = uuid.encode().replace(b'-',b'')
        tmp = binascii.unhexlify(uuid)
        return bytes(reversed(tmp))

    def parse_char_data(self, char_value):
        """
        Chooses correct response for new characteristic value
        """
        data = char_value.split(",")
        size = len(data)
        if (size == 0):
            print ("bad input")
        elif (size == 1):
            self.led_control.turn_off_leds()
        elif (size == 2):
            self.led_control.set_new_data((data[0], data[1], data[1], data[1]))
        elif (size == 4):
            self.led_control.set_new_data((data[0], data[1], data[2], data[3]))
        else:
            print ("wrong number of parameters")
        print (data)
        #print ("Sleeping")
        #machine.deepsleep(15000)
