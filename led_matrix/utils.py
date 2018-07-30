import time

import settings
import led_colors


def display_text(text):
    """Function for writting text directly on the led matrix."""
    print(text)


def get_configured_strip():
    """Return a configured adafruit neopixel led strip."""
    strip = Adafruit_NeoPixel(
        settings.LED_COUNT,
        settings.LED_PIN,
        settings.LED_FREQ_HZ,
        settings.LED_DMA,
        settings.LED_INVERT,
        settings.LED_BRIGHTNESS,
        settings.LED_CHANNEL
    )

    # Intialize the library (must be called once before other functions).
    strip.begin()

    return strip


def map_matrix_to_led_strip(custom_matrix):
    """This function maps a given custom matrix to the led strip as a list of
    colors.

    It assumes that the given matrix is the correct size and that
    leds follow an up than down, right to left pattern starting from
    the bottom right corner.
    This returns a list of led color values.
    """
    led_strip_colors = []

    for column in range(settings.COLUMNS-1, -1, -1):
        if column % 2 == (settings.COLUMNS-1) % 2:
            direction = range(settings.ROWS-1, -1, -1)
        else:
            direction = range(settings.ROWS)

        for row in direction:
            led_strip_colors.append(custom_matrix[row][column])

    return led_strip_colors


def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def set_strip_colors(strip, led_colors):
    """Set the given colors on the led strip."""
    color_wipe(strip, (0, 0, 0), 0)

    for led in range(len(led_colors)):
        strip.setPixelColor(i, *led_colors[i])


class LedMatrixApp(object):

    def __init__(self, *args, **kwargs):
        self.clear_matrix()

    def clear_matrix(self):
        self.matrix = [
            [0 for i in range(settings.ROWS)] for j in range(settings.COLUMNS)]

    def show(self, matrix):
        print('\n'*10)
        for i in range(settings.ROWS):
            print('{}\t|{}|\t{}'.format(i, ' '.join(matrix[i]), i))

    def get_colored_matrix(self, matrix):
        colored_matrix = []
        for line in matrix:
            colored_matrix.append([])
            for element in line:
                if element == 'B':
                    color = led_colors.BLUE
                elif element == 'O':
                    color = led_colors.RED
                else:
                    color = led_colors.EMPTY
                colored_matrix[-1].append(color)