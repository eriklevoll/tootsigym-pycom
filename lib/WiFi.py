from network import WLAN
import _thread
from network_config import saved_networks, ignore_networks
import pycom
import machine
from machine import Timer
import gc
import time


class WiFi:
    """
    WLAN object that handles Wifi scans and connections
    """
    def __init__(self, mqtt):
        """
        Constructor

        Args:
            mqtt:   MQTT object to handle mqtt network
                initialization if WiFi connection succeeds
        """
        self.mqtt       = mqtt
        self.wlan       = WLAN(mode=WLAN.STA)
        self.nets       = self.wlan.scan()
        self.connected  = False

        #Set up 1 second connection test timer
        Timer.Alarm(self.connection_test, 1, periodic=True)

        #Connect Wifi
        _thread.start_new_thread(self.connect, ())

    def connection_test(self, alarm):
        """
        Check WiFi connection state.
        Change PyCom LED correspondingly
        """
        if not self.connected and self.wlan.isconnected():
            self.connected = True
            pycom.rgbled(0x008000)
            gc.collect()
        elif self.connected and not self.wlan.isconnected():
            self.mqtt.stop()
            self.connected = False
            pycom.rgbled(0x800000)
            machine.reset()

    def connect(self):
        """
        Finds suitable networks and connects.
        If connection successful, initialize mqtt
        """
        connected = False
        while not connected:
            connected = self.find_network()
            time.sleep(2)
        print ("WLAN:", self.wlan.isconnected())
        print ("Starting mqtt")
        self.mqtt.start()
        gc.collect()

    def find_network(self):
        """
        """
        print ("Finding networks")
        self.nets = self.wlan.scan()
        time.sleep(0.5)
        print (self.nets)
        saved_network = self.scan_saved_networks()
        print ("Saved network:", saved_network)
        if saved_network is not None:
            connection_state = self.connect_saved_network(saved_network)
            print ("Connection state:", connection_state)
            if connection_state is True: return True

        open_networks = self.scan_open_networks()
        print ("Open networks:", open_networks)
        if open_networks is not None:
            connection_state = self.connect_open_network(open_networks)
            print ("Connection state:", connection_state)
            if connection_state is True: return True

        return False

    def connect_saved_network(self, network):
        """
        """
        network_key         = saved_networks[network][0]
        network_security    = saved_networks[network][1]
        print ("Connecting saved network:", network, network_key, network_security)
        self.wlan.connect(network,
            auth=(network_security, network_key),
            timeout= 5000)

        return self.wait_network_connect()

    def connect_open_network(self, networks):
        """
        """
        print ("Connecting open network")
        connected = False
        for ssid in networks:
            print ("Trying network", ssid)
            self.wlan.connect(ssid, auth=(None, ''), timeout= 5000)
            connected = self.wait_network_connect()
            print ("Connection state:", connected)
            if connected: break

        print ("End of open networks. Connected:", connected)
        return connected

    def wait_network_connect(self, timeout = 10):
        """
        Wait for the network to connect.
        If no connection during timeout, return False. True otherwise
        """
        print ("Waiting for network connection")
        counter = 0
        while not self.wlan.isconnected():
            counter += 1
            print ("Counter:", counter)
            if (counter > timeout): return False
            time.sleep(1)
        print ("Connected:", self.wlan.isconnected())
        return self.wlan.isconnected()


    def scan_saved_networks(self):
        """
        Compares saved networks with scan results.
        Returns one matching network if matches exist, None otherwise
        """
        print ("Scanning saved networks")
        ssid_list = [item.ssid for item in self.nets]
        network_matches = set(saved_networks) & set(ssid_list)
        print ("Matches:", network_matches)
        if len(network_matches) > 0: return next(iter(network_matches))
        else: return None

    def scan_open_networks(self):
        """
        Finds all networks without security
        Returns list of open networks or None if no networks found
        """
        print ("Scanning open networks")
        open_nets = []
        for net in self.nets:
            if net.sec == 0 and not self.in_ignore_networks(net.ssid):
                open_nets.append(net.ssid)

        print ("Found open networks:", open_nets)
        if len(open_nets) == 0: return None
        else: return open_nets

    def in_ignore_networks(self, ssid):
        """
        """
        for keyword in ignore_networks:
            print ("comparing",keyword,ssid)
            if keyword in ssid.lower(): return True

        print ("Bad network")
        return False
