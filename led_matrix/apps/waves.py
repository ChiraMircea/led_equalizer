import time

from neopixel import *
import pyaudio
import numpy as num
import aubio

import led_colors
from settings import *

import struct
import wave

import numpy as np
import pyaudio

from utils import LedMatrixApp


class Waves(LedMatrixApp):
    
    def play(self):
        pass

def make_buckets(raw_list):
    buckets = []

    new_list = raw_list[223:-223]
    buckets = [new_list[x:x+4] for x in range(0, len(new_list), 4)]  

    return buckets


def translate(value, leftMin=0, leftMax=500, rightMin=0, rightMax=16):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    v = rightMin + (valueScaled * rightSpan)
    if v > 250:
        v = 250
    return v


def get_configured_audio_objects():
    """Get the pitch detector and pyaudio objects."""
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    # Aubio's pitch detection.
    pDetection = aubio.pitch("default", 2048,
        2048//2, 44100)

    # Set unit.
    pDetection.set_unit("Hz")
    pDetection.set_silence(-40)

    return stream, pDetection 


def get_basic_example_matrix():
    """This returns a matrix configuration with various strips of color."""
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

    return custom_matrix


def get_romanian_flag_matrix():
    """Romania ftw."""
    custom_matrix = []
    for j in range(254):
        if j < 64:
            custom_matrix.append(led_colors.BLUE)
        elif j < 128:
            custom_matrix.append(led_colors.YELLOW)
        elif j < 192:
            custom_matrix.append(led_colors.RED)
        else:
            custom_matrix.append(led_colors.WHITE)

    return custom_matrix


def equalizer(strip, stream, MAX_y):
    # Read n*nFFT frames from stream, n > 0
    N = max(stream.get_read_available() / nFFT, 1) * nFFT
    data = stream.read(N, exception_on_overflow = False)

    y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
    y_L = y[::2]
    y_R = y[1::2]

    Y_L = np.fft.fft(y_L, nFFT)
    Y_R = np.fft.fft(y_R, nFFT)

    # Sewing FFT of two channels together, DC part uses right channel's
    Y = abs(np.hstack((Y_L[-nFFT / 2:-1], Y_R[:nFFT / 2])))

    ylist = Y.tolist()
    m = make_buckets(ylist)

    return [sum(x)/len(x) for x in m]



def get_band_color(leds):
    """Color leds depending on their 'warmth'.

    Bottom leds will be a cold blue and top leds will be a bright red. Those in
    between will offer a gradient.
    """
    band = []

    for i in range(16):
        if i <= leds:
            if i <= 8:
                if i <= 2:
                    color = (255 - i * 127, 0, i * 127)
                else:
                    color = (0, 42 * (i - 2), 255)
            else:
                color = (0, 255, 255 - 31 * (i-8))
        else:
            color = (0,0,0)
        
        band.append(color)

    return band

if __name__ == '__main__':
    x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

    p = pyaudio.PyAudio()
    MAX_y = 2.0 ** (p.get_sample_size(FORMAT) * 8 - 1)

    frames = None

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=BUF_SIZE,
                    )

    strip = get_configured_strip()
    while True:
      matrix = []
      data = equalizer(strip, stream, MAX_y)

      print("\n\n\n==================================")
      for i in range(len(data)):
        matrix.append([])
        v = int(data[i] * 100)
        if v > 500:
            v = 500
        tv = int(translate(v))
        
        matrix[i] = get_band_color(tv)
        for j in range(16):
            if j <= tv:
                matrix[i].append(led_colors.BLUE)
            else:
                matrix[i].append((0, 0, 0))

        print("{}\t{}\n".format(i, tv))

      c = map_matrix_to_led_strip(matrix)
      set_strip_colors(strip, c)

    stream.stop_stream()
    stream.close()
