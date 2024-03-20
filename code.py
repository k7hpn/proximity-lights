from adafruit_led_animation.animation.rainbow import Rainbow
from math import ceil
from pioasm_neopixel_bg import NeoPixelBackground
from time import monotonic
import adafruit_vl53l1x
import board
import ulab

debug_printing = True

# board pixel, pretty rainbow!
pixel = NeoPixelBackground(board.NEOPIXEL, 1)
pixel.brightness = 0.1
pixel.fill((128, 0, 0))
board_rainbow = Rainbow(pixel, speed=0, period=1, precompute_rainbow=True)

# initialize i2c
i2c = board.STEMMA_I2C()

# initialize the distance sensor
vl53 = adafruit_vl53l1x.VL53L1X(i2c)
vl53.distance_mode = 2
vl53.timing_budget = 500

# set up the neopixel strip
pixels = NeoPixelBackground(board.D2, 60)
pixels.brightness = 1
strip_rainbow = Rainbow(pixels, speed=0, period=1, precompute_rainbow=True)

feet = 0
history = [0] * 10
history_element = 0
last_reading = 0

deviation_differential = 0.05
lights_on = 0
light_status = False

last_time = monotonic()

vl53.start_ranging()

while True:
    if vl53.data_ready:
        distance = vl53.distance
        if (distance != None):
            last_reading = monotonic()
            feet = distance * 0.0328
            history[history_element] = feet
            history_element += 1
            if (history_element > len(history) - 1):
                history_element = 0
        vl53.clear_interrupt()

    deviation = ulab.numpy.std(history)

    if (debug_printing == True):
        if (ceil(last_time) < ceil(monotonic())):
            last_time = monotonic()
            print(f"{monotonic():.0f}: distance {feet} ft deviation {deviation} status {light_status} on {lights_on} last reading {last_reading}")

    if (last_reading + 10 > monotonic() and feet <= 8 and (deviation > deviation_differential or monotonic() < lights_on)):
        pixels.brightness = 0.1
        if (light_status == False or deviation > deviation_differential):
            lights_on = monotonic() + 10
            light_status = True
    else:
        light_status = False
        pixels.brightness = 0

    board_rainbow.animate()
    strip_rainbow.animate()
