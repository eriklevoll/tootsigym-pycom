import time

def increment_color_all(led_control, color, start, end, delay=0, increment=1):
    """
    Change color of all LEDs incrementally

    Args:
        led_control: LED object
        color:      RGB segment to change (string) - red/green/blue
        start:      starting value (int)
        end:        ending value (int)
        delay:      time delay between increments in milliseconds (int)
        increment:  value size to increment each step (int)
    """
    c = start
    while c <= end:
        if (color == "red"):
            r = c
            g = 0
            b = 0
        elif (color == "green"):
            r = 0
            g = c
            b = 0
        else:
            r = 0
            g = 0
            b = c
        led_control.set_all_leds(r,g,b)
        led_control.chain.show(led_control.data)
        c += increment
        #time.sleep(delay/1000.0)

def decrement_color_all(led_control, color, start, end, delay=0, increment=-1):
    """
    Change color of all LEDs incrementally

    Args:
        led_control: LED object
        color:      RGB segment to change (string) - red/green/blue
        start:      starting value (int)
        end:        ending value (int)
        delay:      time delay between increments in milliseconds (int)
        increment:  value size to increment each step (int)
    """
    c = start
    while c >= end:
        if (color == "red"):
            r = c
            g = 0
            b = 0
        elif (color == "green"):
            r = 0
            g = c
            b = 0
        else:
            r = 0
            g = 0
            b = c
        led_control.set_all_leds(r,g,b)
        led_control.chain.show(led_control.data)
        c += increment
        #time.sleep(delay/1000.0)
