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
from __future__ import division
from robophery.interface.i2c import I2cModule


class Bmp085Module(I2cModule):
    """
    Module for BMP085/BMP180 temperature and pressure sensor.
    """
    DEVICE_NAME = 'bmp085'
    DEVICE_ADDR = 0x77

    # Operating Modes
    BMP085_ULTRALOWPOWER = 0
    BMP085_STANDARD = 1
    BMP085_HIGHRES = 2
    BMP085_ULTRAHIGHRES = 3

    # BMP085 Registers
    BMP085_CAL_AC1 = 0xAA  # R   Calibration data (16 bits)
    BMP085_CAL_AC2 = 0xAC  # R   Calibration data (16 bits)
    BMP085_CAL_AC3 = 0xAE  # R   Calibration data (16 bits)
    BMP085_CAL_AC4 = 0xB0  # R   Calibration data (16 bits)
    BMP085_CAL_AC5 = 0xB2  # R   Calibration data (16 bits)
    BMP085_CAL_AC6 = 0xB4  # R   Calibration data (16 bits)
    BMP085_CAL_B1 = 0xB6  # R   Calibration data (16 bits)
    BMP085_CAL_B2 = 0xB8  # R   Calibration data (16 bits)
    BMP085_CAL_MB = 0xBA  # R   Calibration data (16 bits)
    BMP085_CAL_MC = 0xBC  # R   Calibration data (16 bits)
    BMP085_CAL_MD = 0xBE  # R   Calibration data (16 bits)
    BMP085_CONTROL = 0xF4
    BMP085_TEMPDATA = 0xF6
    BMP085_PRESSUREDATA = 0xF6

    # Commands
    BMP085_READTEMPCMD = 0x2E
    BMP085_READPRESSURECMD = 0x34

    def __init__(self, *args, **kwargs):
        super(Bmp085Module, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))
        self._mode = kwargs.get('mode', self.BMP085_ULTRAHIGHRES)
        if self._mode not in [self.BMP085_ULTRALOWPOWER, self.BMP085_STANDARD, self.BMP085_HIGHRES, self.BMP085_ULTRAHIGHRES]:
            raise ValueError(
                'Unexpected mode value {0}. Set mode to one of BMP085_ULTRALOWPOWER, BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES'.format(self._mode))
        self._load_calibration()

    def _load_calibration(self):
        self.cal_AC1 = self._data.readS16(self.BMP085_CAL_AC1, False)  # INT16
        self.cal_AC2 = self._data.readS16(self.BMP085_CAL_AC2, False)  # INT16
        self.cal_AC3 = self._data.readS16(self.BMP085_CAL_AC3, False)  # INT16
        self.cal_AC4 = self._data.readU16(self.BMP085_CAL_AC4, False)  # UINT16
        self.cal_AC5 = self._data.readU16(self.BMP085_CAL_AC5, False)  # UINT16
        self.cal_AC6 = self._data.readU16(self.BMP085_CAL_AC6, False)  # UINT16
        self.cal_B1 = self._data.readS16(self.BMP085_CAL_B1, False)    # INT16
        self.cal_B2 = self._data.readS16(self.BMP085_CAL_B2, False)    # INT16
        self.cal_MB = self._data.readS16(self.BMP085_CAL_MB, False)    # INT16
        self.cal_MC = self._data.readS16(self.BMP085_CAL_MC, False)    # INT16
        self.cal_MD = self._data.readS16(self.BMP085_CAL_MD, False)    # INT16
#        self._log.debug('AC1 = {0:6d}'.format(self.cal_AC1))
#        self._log.debug('AC2 = {0:6d}'.format(self.cal_AC2))
#        self._log.debug('AC3 = {0:6d}'.format(self.cal_AC3))
#        self._log.debug('AC4 = {0:6d}'.format(self.cal_AC4))
#        self._log.debug('AC5 = {0:6d}'.format(self.cal_AC5))
#        self._log.debug('AC6 = {0:6d}'.format(self.cal_AC6))
#        self._log.debug('B1 = {0:6d}'.format(self.cal_B1))
#        self._log.debug('B2 = {0:6d}'.format(self.cal_B2))
#        self._log.debug('MB = {0:6d}'.format(self.cal_MB))
#        self._log.debug('MC = {0:6d}'.format(self.cal_MC))
#        self._log.debug('MD = {0:6d}'.format(self.cal_MD))

    def _load_datasheet_calibration(self):
        """
        Set calibration from values in the datasheet example. Useful for
        debugging the temperature and pressure calculation accuracy.
        """
        self.cal_AC1 = 408
        self.cal_AC2 = -72
        self.cal_AC3 = -14383
        self.cal_AC4 = 32741
        self.cal_AC5 = 32757
        self.cal_AC6 = 23153
        self.cal_B1 = 6190
        self.cal_B2 = 4
        self.cal_MB = -32767
        self.cal_MC = -8711
        self.cal_MD = 2868

    def read_raw_temp(self):
        """
        Read the raw (uncompensated) temperature from the sensor.
        """
        self._data.write8(self.BMP085_CONTROL, self.BMP085_READTEMPCMD)
        self._msleep(5)  # Wait 5ms
        raw = self._data.readU16(self.BMP085_TEMPDATA, False)
#        self._log.debug('Raw temp 0x{0:X} ({1})'.format(raw & 0xFFFF, raw))
        return raw

    def read_raw_pressure(self):
        """
        Read the raw (uncompensated) pressure level from the sensor.
        """
        self._data.write8(self.BMP085_CONTROL,
                    self.BMP085_READPRESSURECMD + (self._mode << 6))
        if self._mode == self.BMP085_ULTRALOWPOWER:
            self._msleep(5)
        elif self._mode == self.BMP085_HIGHRES:
            self._msleep(14)
        elif self._mode == self.BMP085_ULTRAHIGHRES:
            self._msleep(26)
        else:
            self._msleep(8)
        msb = self._data.readU8(self.BMP085_PRESSUREDATA)
        lsb = self._data.readU8(self.BMP085_PRESSUREDATA + 1)
        xlsb = self._data.readU8(self.BMP085_PRESSUREDATA + 2)
        raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self._mode)
        # self._log.debug('Raw pressure 0x{0:04X} ({1})'.format(raw & 0xFFFF, raw))
        return raw

    def read_temperature(self):
        """
        Get the compensated temperature in degrees celsius.
        """
        UT = self.read_raw_temp()
        # Datasheet value for debugging:
        # UT = 27898
        # Calculations below are taken straight from section 3.5 of the
        # datasheet.
        X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
        temp = ((B5 + 8) >> 4) / 10.0
#        self._log.debug('Calibrated temperature {0} C'.format(temp))
        return temp

    def read_pressure(self):
        """
        Get the compensated pressure in Pascals.
        """
        UT = self.read_raw_temp()
        UP = self.read_raw_pressure()
        # Datasheet values for debugging:
        # UT = 27898
        # UP = 23843
        # Calculations below are taken straight from section 3.5 of the datasheet.
        # Calculate true temperature coefficient B5.
        X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
#        self._log.debug('B5 = {0}'.format(B5))
        # Pressure Calculations
        B6 = B5 - 4000
#        self._log.debug('B6 = {0}'.format(B6))
        X1 = (self.cal_B2 * (B6 * B6) >> 12) >> 11
        X2 = (self.cal_AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.cal_AC1 * 4 + X3) << self._mode) + 2) // 4
#        self._log.debug('B3 = {0}'.format(B3))
        X1 = (self.cal_AC3 * B6) >> 13
        X2 = (self.cal_B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.cal_AC4 * (X3 + 32768)) >> 15
#        self._log.debug('B4 = {0}'.format(B4))
        B7 = (UP - B3) * (50000 >> self._mode)
#        self._log.debug('B7 = {0}'.format(B7))
        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2
        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        p = p + ((X1 + X2 + 3791) >> 4)
#        self._log.debug('Pressure {0} Pa'.format(p))
        return p

    def read_altitude(self, sealevel_pa=101325.0):
        """
        Calculate the altitude in meters.
        """
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0 / 5.255)))
#        self._log.debug('Altitude {0} m'.format(altitude))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """
        Calculate the pressure at sealevel when given a known altitude in
        meters. Return a value in Pascals.
        """
        pressure = float(self.read_pressure())
        p0 = pressure / pow(1.0 - altitude_m / 44330.0, 5.255)
        return int(p0)

    def read_data(self):
        """
        Get all sensor readings.
        """
        read_start = self._get_time()
        try:
            temp = self.read_temperature()
        except IOError:
            temp = None
        read_stop = self._get_time()
        temp_read_time = read_stop - read_start
        read_start = self._get_time()
        try:
            press = self.read_pressure()
        except IOError:
            press = None
        read_stop = self._get_time()
        press_read_time = read_stop - read_start
        data = [
            (self._name, 'temperature', temp, temp_read_time),
            (self._name, 'pressure', press, press_read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'temperature': {
                'type': 'gauge',
                'unit': 'C',
                'precision': 2,
                'range_low': -40,
                'range_high': 85,
                'sensor': self.DEVICE_NAME
            },
            'pressure': {
                'type': 'gauge',
                'unit': 'Pa',
                'precision': 3,
                'range_low': 30000,
                'range_high': 110000,
                'sensor': self.DEVICE_NAME
            }
        }
