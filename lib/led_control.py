from NeoPixel import WS2812

NUM_OF_LED_ROWS = 18
NUM_OF_LED_COLS = 11

HOLDS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #18
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #17
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #16
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #15
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #14
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #13
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #12
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #11
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #10
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #9
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #8
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #7
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #6
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #5
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #4
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #3
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #2
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   #1
]
#   A   B   C   D   E   F   G   H   I   J   K

class Control:
    def __init__(self, num_of_leds, initial_state = (0,0,0)):
        """
        Constructor

        Args:
            num_of_leds: number of leds to control
        """
        self.chain = WS2812(ledNumber=num_of_leds, intensity=1)
        self.num_of_leds = num_of_leds
        self.data = [initial_state] * num_of_leds
        self.led_count = len(HOLDS)
        print ("leds: ", self.led_count)
        self.holds_dict = { }
        self.leds_state = { 'start': [], 'mid': [], 'top': [] }

        self.calculate_holds()

        self.start()

    def calculate_holds(self):
        """
        Calculate led indices for existing holds according to HOLDS list
        """
        true_counter = 1
        for i in range(len(HOLDS)):
            if (HOLDS[i] == False): continue
            self.holds_dict[i+1] = true_counter
            true_counter += 1

    def start(self):
        """
        Initialize LED data protocol
        """
        self.chain.show(self.data)

    def set_all_leds(self, r, g, b):
        """
        Change color value for all leds simultaneously
        """

        #Clear any current routes
        self.leds_state = { 'start': [], 'mid': [], 'top': [] }

        for index in range(self.num_of_leds):
            self.data[index] = (r,g,b)

    def turn_off_leds(self):
        """
        Set led color to 0,0,0
        """
        self.set_all_leds(0,0,0)

    def set_route(self, data):
        """
        Turn on leds green/blue/red corresponding to a specific route
        """
        datalist = data.split(";")
        self.set_all_leds(0,0,0)
        self.set_route_color(datalist[0], (0,255,0))
        self.set_route_color(datalist[1], (0,0,255))
        self.set_route_color(datalist[2], (255,0,0))

        self.chain.show(self.data)

    def set_route_color(self, data, color):
        """
        Submethod for setting hold leds for one color
        """
        try:
            for rc in data.split(","):
                self.update_leds_state(rc, color[0], color[1], color[2])
                hold_index = self.get_index(rc) - 1
                self.data[hold_index] = color
        except:
            print ("Failed to set color for", color, rc, data)

    def set_new_data(self, new_data):
        """
        Change led color
        """
        #rc = int(new_data[0])
        rc = new_data[0]
        r  = int(new_data[1])
        g  = int(new_data[2])
        b  = int(new_data[3])

        if rc == "-1": i = -1
        else: i = self.get_index(rc) - 1

        if self.check_valid_data(i, r, g, b) == False: return
        #print ("index: ", i)
        if i < 0:
            self.set_all_leds(r,g,b)
        else:
            self.data[i] = (r,g,b)
            self.update_leds_state(rc, r, g, b)

        self.chain.show(self.data)

    def update_leds_state(self, rc, r, g, b):
        """
        """
        #remove and previous occurrences
        self.remove_led_element(rc)

        if (r > 0 and g == 0 and b == 0):
            self.add_led_element(rc, 'top')
        elif (r == 0 and g > 0 and b == 0):
            self.add_led_element(rc, 'start')
        elif (r == 0 and g == 0 and b > 0):
            self.add_led_element(rc, 'mid')

        # print (self.leds_state)

    def remove_led_element(self, rc):
        """
        """
        try:
            for hold_type in self.leds_state:
                if rc in self.leds_state[hold_type]:
                    self.leds_state[hold_type].remove(rc)
        except:
            print ("Failed to remove element", rc)

    def add_led_element(self, rc, hold_type):
        """
        """
        try:
            self.leds_state[hold_type].append(rc)
        except:
            print ("Failed to add new element", rc, hold_type)

    def compose_status_response(self):
        """
        """
        resp_data = ""
        for hold in self.leds_state['start']:
            resp_data += hold + ","
        resp_data += ";"
        for hold in self.leds_state['mid']:
            resp_data += hold + ","
        resp_data += ";"
        for hold in self.leds_state['top']:
            resp_data += hold + ","

        if (resp_data[-1] == ','): resp_data = resp_data[:-1]
        resp_data = resp_data.replace(",;", ";")

        # print (resp_data)

        return resp_data

    def get_index(self, rc):
        """
        Extracts row and column values from input
        and returns corresponding LED index
        """
        try:
            col = ord(rc[0]) - 64
            row = int(rc[1:])
            return self.convert_rc_to_index(row, col)
        except:
            return -1

    def convert_rc_to_index(self, row, col):
        """
        Calculate LED index from row column values
        """
        if (row % 2 == 0):
            return NUM_OF_LED_COLS * (row - 1) + col
        else:
            return NUM_OF_LED_COLS * row + 1 - col

    def check_valid_data(self, index, r, g, b):
        """
        Checks if new LED data format is correct

        Returns True if correct, False otherwise
        """
        valid = True
        if (index >= self.num_of_leds):
            print ("bad index", index, self.num_of_leds)
            valid = False
        if (r < 0 or r > 255):
            print ("bad color value (r)", r)
            valid = False
        if (g < 0 or g > 255):
            print ("bad color value (g)", g)
            valid = False
        if (b < 0 or b > 255):
            print ("bad color value (b)", b)
            valid = False

        return valid
