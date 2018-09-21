import _thread
from network_config import mqtt_config
from umqtt import MQTTClient
import gc

class MQTT:
    def __init__(self, led_control, device_name):
        """
        Constructor
        """

        self.led_control    = led_control
        self.topic          = mqtt_config['topic']
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
        self.client.connect()
        print ("Subscribing")
        self.client.subscribe(topic=self.topic)

        self.client.set_last_will(self.topic, "Bye")

        print ("Listening")
        _thread.start_new_thread(self.start_listening, ())

        gc.collect()

    def stop(self):
        """
        Disconnect and stop listening
        """
        self.client.disconnect()

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
        data = data.decode('utf-8').split(",")
        print (data)
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

    def start_listening(self):
        while True:
            self.client.check_msg()
            gc.collect()
