# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
try:
    import Adafruit_BBIO.PWM
except ImportError:
    raise RuntimeError(
        "Cannot load Adafruit_BBIO.PWM library. Please install the library.")

from robophery.interface.pwm import PwmInterface


class BeaglebonePwmInterface(PwmInterface):
    """
    PWM implementation for the BeagleBone Black using the Adafruit_BBIO.PWM
    library.
    """
    AVAILABLE_PINS = [
        'P8_13',
        'P8_19',
        'P8_34',
        'P8_36',
        'P8_45',
        'P8_46',
        'P9_14',
        'P9_16',
        'P9_21',
        'P9_22',
        'P9_28',
        'P9_29',
        'P9_31',
        'P9_42',
    ]

    def __init__(self, *args, **kwargs):
        self._bus = Adafruit_BBIO.PWM
        self._pins_available = self.AVAILABLE_PINS
        super(BeaglebonePwmInterface, self).__init__(*args, **kwargs)

    def setup_pin(self, pin, dutycycle, frequency=2000):
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError(
                'Invalid duty cycle value, must be between 0 and 100.')
        self._bus.start(pin, dutycycle, frequency)

    def set_duty_cycle(self, pin, dutycycle):
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError(
                'Invalid duty cycle value, must be between 0 and 100.')
        self._bus.set_duty_cycle(pin, dutycycle)

    def set_frequency(self, pin, frequency):
        self._bus.set_frequency(pin, frequency)

    def stop(self, pin):
        self._bus.stop(pin)
