NUM_OF_LED_ROWS = 18
NUM_OF_LED_COLS = 11

HOLDS = [
#   A   B   C   D   E   F   G   H   I   J   K
    0   0   0   0   0   0   0   0   0   0   0   #18
    0   0   0   0   0   0   0   0   0   0   0   #17
    0   0   0   0   0   0   0   0   0   0   0   #16
    0   0   0   0   0   0   0   0   0   0   0   #15
    0   0   0   0   0   0   0   0   0   0   0   #14
    0   0   0   0   0   0   0   0   0   0   0   #13
    0   0   0   0   0   0   0   0   0   0   0   #12
    0   0   0   0   0   0   0   0   0   0   0   #11
    0   0   0   0   0   0   0   0   0   0   0   #10
    0   0   0   0   0   0   0   0   0   0   0   #9
    0   0   0   0   0   0   0   0   0   0   0   #8
    0   0   0   0   0   0   0   0   0   0   0   #7
    0   0   0   0   0   0   0   0   0   0   0   #6
    0   0   0   0   0   0   0   0   0   0   0   #5
    0   0   0   0   0   0   0   0   0   0   0   #4
    0   0   0   0   0   0   0   0   0   0   0   #3
    0   0   0   0   0   0   0   0   0   0   0   #2
    0   0   0   0   0   0   0   0   0   0   0   #1
]


LED_HOLDS = [
    #A      #B      #C      #D      #E      #F      #G      #H      #I      #J      #K
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #18
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #17
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #16
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #15
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #14
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #13
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #12
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #11
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #10
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #9
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #8
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #7
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #6
    True,   False,   True,  True,   False,   False,  False,   False,  False,   False,  False,   #5
    False,  False,  False,  False,  False,  False,  False,  False,  False,  False,  False,   #4
    False,   False,   False,  False,   False,   False,  False,   False,  False,   False,  False,   #3
    False,  False,  False,  False,  False,  False,  False,  False,  False,  False,  False,   #2
    False,  False,  False,  False,  False,  False,  False,  False,  False,  False,  False   #1
]

class Control:
    def __init__(self, chain, num_of_leds, initial_state = (0,0,0)):
        """
        Constructor

        Args:
            chain: WS2812 control object
            num_of_leds: number of leds to control
        """
        self.num_of_leds = num_of_leds
        self.chain = chain
        self.data = [initial_state] * num_of_leds
<<<<<<< HEAD
        self.led_count = len(LED_HOLDS)
        print ("leds: ", self.led_count)
=======
        self.holds_dict = {}

        self.calculate_holds()

    def calculate_holds(self):
        """
        Calculate led indices for existing holds according to HOLDS list
        """
        true_counter = 1
        for i in range(len(HOLDS)):
            if (HOLDS[i] == False): continue
            self.holds_dict[i+1] = true_counter
            true_counter += 1

>>>>>>> 6c8e37f9b883069f02d3db08f6a7547fa4a5ca6b

    def start(self):
        """
        Initialize LED data protocol
        """
        self.chain.show(self.data)

    def set_all_leds(self, r, g, b):
        """
        Change color value for all leds simultaneously
        """

        for index in range(self.num_of_leds):
            self.data[index] = (r,g,b)
    def turn_off_leds(self):
        """
        Set led color to 0,0,0
        """
        self.set_all_leds(0,0,0)
        self.chain.show(self.data)

    def set_new_data(self, new_data):
        """
        Change led color
        """
        rc = int(new_data[0])
        r  = int(new_data[1])
        g  = int(new_data[2])
        b  = int(new_data[3])

        i = get_index(rc)

        if self.check_valid_data(i, r, g, b) == False: return

        if i < 0:
            self.set_all_leds(r,g,b)
        else:
            led_index = holds_dict[i]
            self.data[led_index] = (r,g,b)

        self.chain.show(self.data)

    def get_index(self, rc):
        """
        Extracts row and column values from input
        and returns corresponding LED index
        """
        try:
            col = ord(rc[0]) - 64
            row = int(rc[1:])
            return convert_rc_to_index(row, col)
        except:
            return: -1

    def convert_rc_to_index(self, row, col):
        """
        Calculate LED index from row column values
        """
        if (row % 2 == 0):
            return NUM_OF_LED_COLS * row + 1 - col
        else:
            return NUM_OF_LED_COLS * (row - 1) + c


    def check_valid_data(self, index, r, g, b):
        """
        Checks if new LED data format is correct

        Returns False if correct, False otherwise
        """
        valid = False
        if (index >= self.num_of_leds):
            print ("bad index", index)
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
