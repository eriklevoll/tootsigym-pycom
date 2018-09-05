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
        #self.scanning       = False
        #self.scanning_timer = Timer.Alarm(self.scan_timer_elapsed, s=3, periodic=True)
        self.devices_dict   = {}

        #self.bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.connection_callback)
        self.bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.NEW_ADV_EVENT, handler=self.connection_callback)

    def start_scan(self):
        self.bluetooth.start_scan(-1)

    def connection_callback(self, bt_o):
        """
        Callback function for bluetooth connection triggers (connected/disconnected)
        """
        events = bt_o.events()
        if  events & Bluetooth.CLIENT_CONNECTED:
            print("Device connected", bt_o)
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            print("Device disconnected")
        elif events & Bluetooth.NEW_ADV_EVENT:
            print ("Got something")
            self.parse_adv()

    def parse_adv(self):
        adv = self.bluetooth.get_adv()
        if not adv: return

        device_name = self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        if "MB_APP" in device_name:
            id = device_name.split(":::")[1]
            if (id in self.devices_dict):
                print ("juba on", id, self.devices_dict)
                return
            print (id, self.devices_dict)
            print ("Connecting")
            conn = self.bluetooth.connect(adv.mac)
            self.devices_dict[id] = conn
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
                            char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)
                            char.write(b'CONN_OK')
                        print ("val:", val, val == id)

            print ("Started scanning again")
            self.bluetooth.start_scan(-1)
            time.sleep(1)

    # def scan(self, enabled):
    #     """
    #     Enables or disables bluetooth scanning
    #
    #     Args:
    #         enabled: True or False
    #     """
    #     try:
    #         if enabled:
    #             self.bluetooth.start_scan(-1)
    #             self.scanning = True
    #         else:
    #             self.bluetooth.stop_scan()
    #             self.scanning = False
    #     except:
    #         print ("Failed to set scanning:", enabled)


    def characteristic_callback(self, characteristic):
        print ('Bluetooth.CHAR_NOTIFY_EVENT')
        char_value = characteristic.value().decode('utf-8')
        print (char_value)
        if ("disconnect" in char_value):
            device_id = char_value.split(":::")[1]
            conn = self.devices_dict[device_id]
            conn.disconnect()
            del self.devices_dict[device_id]

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

    def detect_write_event(self, value):
        """
        Chooses correct response for new characteristic value
        """
        val = value.decode("utf-8").split(",")
        size = len(val)
        if (size == 0):
            print ("bad input")
        elif (size == 1):
            self.led_control.turn_off_leds()
        elif (size == 2):
            self.led_control.set_new_data((val[0], val[1], val[1], val[1]))
        elif (size == 4):
            self.led_control.set_new_data((val[0], val[1], val[2], val[3]))
        else:
            print ("wrong number of parameters")
        print (val)
