import math
from robophery.interface.i2c import I2cModule


class Htu21dModule(I2cModule):
    """
    Module for HTU21D temperature and humidity sensor.
    """
    DEVICE_NAME = 'htu21d'
    # HTU21D default address
    DEVICE_ADDR = 0x40
    # Operating modes
    HOLD_MASTER = 0x00
    NOHOLD_MASTER = 0x10
    # HTU21D commands
    HTU21D_TRIGGERTEMPCMD = 0xE3  # Trigger Temperature Measurement
    HTU21D_TRIGGERHUMIDITYCMD = 0xE5  # Trigger Humidity Measurement
    HTU21D_WRITEUSERCMD = 0xE6  # Write user register
    HTU21D_READUSERCMD = 0xE7  # Read user register
    HTU21D_SOFTRESETCMD = 0xFE  # Soft reset
    # HTU21D constants for Dew Point calculation
    HTU21D_A = 8.1332
    HTU21D_B = 1762.39
    HTU21D_C = 235.66

    def __init__(self, *args, **kwargs):
        super(Htu21dModule, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))
        # Check that mode is valid.
        self._mode = kwargs.get('mode', self.HOLD_MASTER)
        if self._mode not in [self.HOLD_MASTER, self.NOHOLD_MASTER]:
            raise ValueError('Unexpected mode value {0}.'.format(self._mode))

    def crc_check(self, msb, lsb, crc):
        remainder = ((msb << 8) | lsb) << 8
        remainder |= crc
        divsor = 0x988000
        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1
        if remainder == 0:
            return True
        else:
            return False

    def get_raw_temp(self):
        """
        Reads the raw temperature from the sensor.
        """
        msb, lsb, chsum = self._data.readList(self.HTU21D_TRIGGERTEMPCMD, 3)
        if self.crc_check(msb, lsb, chsum) is False:
            raise RuntimeError("CRC Exception")
        raw = (msb << 8) + lsb
        raw &= 0xFFFC
        return raw

    def get_raw_humidity(self):
        """
        Reads the raw relative humidity from the sensor.
        """
        msb, lsb, chsum = self._data.readList(self.HTU21D_TRIGGERHUMIDITYCMD, 3)
        if self.crc_check(msb, lsb, chsum) is False:
            raise RuntimeError("CRC Exception")
        raw = (msb << 8) + lsb
        raw &= 0xFFFC
        return raw

    def get_temperature(self):
        """
        Gets the temperature in degrees celsius.
        """
        raw = self.get_raw_temp()
        temp = float(raw) / 65536 * 175.72
        temp -= 46.85
        return temp

    def get_humidity(self):
        """
        Gets the relative humidity.
        """
        raw = self.get_raw_humidity()
        rh = float(raw) / 65536 * 125
        rh -= 6
        return rh

    def get_dew_point(self):
        """
        Calculates the dew point temperature.
        """
        den = math.log10(self.get_humidity() *
                         self.get_partial_pressure() / 100) - self.HTU21D_A
        dew = -(self.HTU21D_B / den + self.HTU21D_C)
        return dew

    def get_partial_pressure(self):
        """
        Calculate the partial pressure in mmHg at ambient temperature.
        """
        Tamb = self.get_temperature()
        exp = self.HTU21D_B / (Tamb + self.HTU21D_C)
        exp = self.HTU21D_A - exp
        pp = 10 ** exp
        return pp

    def read_data(self):
        """
        Get all sensor readings.
        """
        temp_time_start = self._get_time()
        try:
            temp = self.get_temperature()
        except IOError:
            temp = None
        temp_time_stop = self._get_time()
        temp_time_delta = temp_time_stop - temp_time_start
        humid_time_start = self._get_time()
        try:
            humid = self.get_humidity()
        except IOError:
            humid = None
        humid_time_stop = self._get_time()
        humid_time_delta = humid_time_stop - humid_time_start
        data = [
            (self._name, 'temperature', temp, temp_time_delta),
            (self._name, 'humidity', humid, humid_time_delta),
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
                'precision': 0.25,
                'range_low': -40,
                'range_high': 125,
                'sensor': self.DEVICE_NAME
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'precision': 5,
                'range_low': 0,
                'range_high': 100,
                'sensor': self.DEVICE_NAME
            },
        }
