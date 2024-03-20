# proximity-lights

CircuitPython code to light up Neopixels when proximity changes as read from a time-of-flight ranging sensor.

## Necessary parts

Connect the following with STEMMA QT cable:

- STEMMA QT board running CircuitPython 9
- VL53L1X Time-of-Flight ranging sensor
- String of NeoPixels (60 by default) to pin D2 (customize this on line 26)

## How it works

1. The on-board NeoPixel will cycle the rainbow to indicate the board is working
2. Distances will be read from the time-of-flight sensor via I2C
3. When the standard deviation of distance measurements passes a threshhold, the lights will turn on
4. When the standard deviation zeros out, the lights remain on for 10 seconds and then turn off

## References

The following files should live in `lib/` and be appropriate for the version of CircuitPython you are using:

- `adafruit_led_animation`
- `adafruit_pioasm.mpy`
- `adafruit_vl53l1x.mpy`
- [`pioasm_neopixel_bg.py`](https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/advanced-using-pio-to-drive-neopixels-in-the-background)

## License

This code is released under the [MIT License](https://github.com/k7hpn/proximity-lights/blob/main/LICENSE)
