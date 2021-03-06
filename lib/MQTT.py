import _thread
from network_config import mqtt_config
from umqtt import MQTTClient
import gc
import time
from machine import Timer
import pycom

class MQTT:
    def __init__(self, led_control, device_name):
        """
        Constructor
        """

        self.led_control    = led_control
        self.topic          = mqtt_config['topic']
        self.resp_topic     = mqtt_config['resp_topic']
        self.device_name    = device_name

    def start(self):
        """
        Initialize MQTT Connection
        """
        print ("Creating client")
        self.client = MQTTClient(
                                client_id   = self.device_name,
                                server      = mqtt_config['address'],
                                user        = mqtt_config['username'],
                                password    = mqtt_config['user_key'],
                                port        = mqtt_config['port'])
        print ("Setting timeout")
        self.client.settimeout = self.set_timeout
        print ("Setting callback")
        self.client.set_callback(self.sub_cb)
        print ("Connecting mqtt", mqtt_config['address'], mqtt_config['username'], mqtt_config['user_key'], mqtt_config['port'])
        res = self.client.connect()
        if (res == -1):
            print ("Failed to connect")
            pycom.rgbled(0xB900B9)
            return
        print ("Subscribing")
        self.client.subscribe(topic=self.topic)

        self.client.set_last_will(self.resp_topic, "Bye")

        print ("Listening")
        pycom.rgbled(0x00ff00)

        Timer.Alarm(self.check_new_messages, 0.0075, periodic=True)

        gc.collect()

    def stop(self):
        """
        Disconnect and stop listening
        """
        self.client.disconnect()

    def send_data(self, data):
        self.client.publish(topic=self.resp_topic, msg=data)

    def sub_cb(self, topic, message):
        """
        """
        if message is None: return
        else: self.parse_input_data(message)

    def set_timeout(duration):
        """
        """
        pass

    def parse_input_data(self, data):
        """
        Chooses correct response for new characteristic value
        """
        decoded = data.decode('utf-8')
        #Echo data back to MQTT backend

        if "status" in decoded:
            resp_data = self.led_control.compose_status_response()
            self.send_data("resp:" + resp_data)
            return

        # print (decoded)

        self.send_data("resp:" + decoded)

        if ";" in decoded:
            self.led_control.set_route(decoded)
            return
        if ("," not in decoded): return
        data = decoded.split(",")
        #print (data)
        size = len(data)
        if (size == 0):
            print ("bad input")
            return

        if (size == 1):
            self.led_control.turn_off_leds()
        elif (size == 2):
            self.led_control.set_new_data((data[0], data[1], data[1], data[1]))
        elif (size == 4):
            self.led_control.set_new_data((data[0], data[1], data[2], data[3]))

    def check_new_messages(self, alarm):
        self.client.check_msg()
