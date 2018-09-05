from network import Bluetooth
from utilities import increment_color_all, decrement_color_all
from machine import Timer
import time
import binascii
import machine
import _thread

NORMAL_OPERATION        =   b'\x00'
DISABLE_NETWORK_DATA    =   b'\x01'
ENABLE_NETWORK_DATA     =   b'\x02'
OPEN_LASERS             =   b'\x03'
CLOSE_LASERS            =   b'\x04'
VIEW_LASER_DATA         =   b'\x05'
HIDE_LASER_DATA         =   b'\x06'
UPDATE_OTA              =   b'\x07'
SEND_ONETIME            =   b'\x08'


class BLE:
    def __init__(self, led_control):
        """
        Constructor

        Args:
            led_control:   LED control object
        """
        self.led_control    = led_control
        self.bluetooth      = Bluetooth()
        self.scanning       = False
        self.scanning_timer = Timer.Alarm(self.scan_timer_elapsed, s=3, periodic=True)
        self.devices_dict   = {}

        #self.bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.connection_callback)
        self.bluetooth.callback(trigger = Bluetooth.NEW_ADV_EVENT, handler = self.new_adv_event)

    def new_adv_event(self, event):
        if event.events() == Bluetooth.NEW_ADV_EVENT:
            adv = self.bluetooth.get_adv()
            device_name = self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)

            if (device_name is None): return
            if ("MB_APP" not in device_name): return

            device_id = self.get_device_id(device_name)

            if (device_id in self.devices_dict): return

            print (device_name, adv.mac)
            connection = self.bluetooth.connect(adv.mac)
            self.devices_dict[device_id] = connection
            #
            services = connection.services()
            for service in services:
                if (type(service.uuid()) is bytes):
                    chars = service.characteristics()
                    for char in chars:
                        if (type(char.uuid()) is bytes):
                            print ("Set callback")
                            char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)
            #     print (service.uuid())
            #     if (type(service.uuid()) is bytes):
            #         service.characteristics()
                #for char in chars:
            #        pass

            #time.sleep(0.1)
            #self.bluetooth.start_scan(-1)
            #     print (service)
            #         print (char)
            #         if (type(char.uuid()) is bytes):
            #             char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)
            #self.set_notify_listener(services)
            # for service in services:
            #     chars = service.characteristics()
            #     for char in chars:
            #         if (type(char.uuid()) is bytes):
            #             char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)

    def set_notify_listener(self, services):
        try:
            for service in services:
                chars = service.characteristics()
                for char in chars:
                    if (type(char.uuid()) is bytes):
                        char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)
        except:
            print ("Failed to set notify listener")

    def connection_callback(self, bt_o):
        """
        Callback function for bluetooth connection triggers (connected/disconnected)
        """
        events = bt_o.events()
        if  events & Bluetooth.CLIENT_CONNECTED:
            print("Device connected")
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            print("Device disconnected")

    def scan(self, enabled):
        """
        Enables or disables bluetooth scanning

        Args:
            enabled: True or False
        """
        try:
            if enabled:
                self.bluetooth.start_scan(-1)
                self.scanning = True
            else:
                self.bluetooth.stop_scan()
                self.scanning = False
        except:
            print ("Failed to set scanning:", enabled)

    def test_thread(self, ble, adv):
        device_name = ble.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        if not device_name: return

        device_id = self.get_device_id(device_name)

        print ("Connecting")
        connection = ble.connect(adv.mac)

        print (device_id)

    def scan_timer_elapsed(self, _):
        """
        Periodic scanning timer method. Read and parse scan results here.
        """
        #print ("Scanning:",self.bluetooth.isscanning())

        #if not self.bluetooth.isscanning():
    #        self.bluetooth.start_scan(-1)

        #
        # adv = self.bluetooth.get_adv()
        # print (adv, self.bluetooth.isscanning(), self.devices_dict)
        #
        # if not adv:
        #     pass
        # else:
        #     _thread.start_new_thread(self.test_thread, (self.bluetooth, adv))
            #self.test_thread(self.bluetooth, adv)
            #self.parse_scan_result(adv)

    def disconnect_device(self, device_id):
        connection = self.devices_dict[device_id]
        connection.disconnect()
        del self.devices_dict[device_id]
        print ("stopped")

    def parse_scan_result(self, adv):
        """
        Read available device services and characteristics.
        """
        device_name = self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        #Make sure name is not null
        if not device_name: return

        try:
            device_id = self.get_device_id(device_name)
            #Make sure device is already not connected
            if device_id in self.devices_dict:
                print ("Device already added")
                return
            print (device_id)
            print ("Connecting")

            connection = self.bluetooth.connect(adv.mac)

            services = connection.services()
            connection_established  = False
            for service in services:
                chars = service.characteristics()
                for char in chars:
                    if (type(char.uuid()) is bytes):
                        self.devices_dict[device_id] = connection
                        connection_established = True
                        char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=self.characteristic_callback)
        except:
            print ("Failed to parse device data")

    def characteristic_callback(self, characteristic):
        print ('Bluetooth.CHAR_NOTIFY_EVENT')
        val = characteristic.value().decode('utf-8')
        print (val)
        if ("disconnect" in val):
            v2 = val.split(":::")[1]
            print (v2)
            self.disconnect_device(v2)
        else:
            characteristic.write(b'response')

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
