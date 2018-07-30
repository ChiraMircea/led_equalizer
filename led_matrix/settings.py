# import pyaudio


# Matrix
ROWS = 16
COLUMNS = 16

# LED strip
LED_COUNT      = 264     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Audio
SAVE = 0.0
TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = 25.0
nFFT = 512
BUF_SIZE = 4 * nFFT
# FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

