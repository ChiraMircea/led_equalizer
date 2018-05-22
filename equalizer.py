import time

from neopixel import *

import led_colors
from settings import ROWS, COLUMNS


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
    """This function maps a given custom matrix to the led strip.

    It assumes that the given matrix is the correct size and that
    leds follow an up than down, right to left pattern starting from
    the bottom right corner.
    This returns a list of led color values.
    """
    led_strip_colors = []

    for column in range(COLUMNS-1, -1, -1):
        if column % 2 == (COLUMNS-1) % 2:
            direction = range(ROWS-1, -1, -1)
        else:
            direction = range(ROWS)

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

    for led in range(len(led_colors):
        strip.setPixelColor(i, *led_colors[i])
        time.sleep(0.05)

if __name__ == '__main__':
    custom_matrix = [
        [led_colors.RED] * 16,
        [led_colors.BLUE] * 16,
        [led_colors.GREEN] * 16,
        [led_colors.RED] * 16,
        [led_colors.RED] * 16,
        [led_colors.BLUE] * 16,
        [led_colors.GREEN] * 16,
        [led_colors.RED] * 16,
        [led_colors.RED] * 16,
        [led_colors.BLUE] * 16,
        [led_colors.GREEN] * 16,
        [led_colors.RED] * 16,
        [led_colors.RED] * 16,
        [led_colors.BLUE] * 16,
        [led_colors.GREEN] * 16,
        [led_colors.RED] * 16
    ]

    strip = get_configured_strip()
    led_colors = map_matrix_to_led_strip(custom_matrix)
    set_strip_colors(strip, led_colors)
    strip.show()

