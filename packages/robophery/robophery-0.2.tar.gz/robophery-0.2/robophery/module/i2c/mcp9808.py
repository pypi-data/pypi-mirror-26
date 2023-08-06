from robophery.interface.i2c import I2cModule


class Mcp9808Module(I2cModule):
    """
    Module for MCP9808 temperature sensor.
    """
    DEVICE_NAME = 'mcp9808'
    DEVICE_ADDR = 0x18

    MCP9808_REG_CONFIG_SHUTDOWN = 0x0100
    MCP9808_REG_CONFIG_CRITLOCKED = 0x0080
    MCP9808_REG_CONFIG_WINLOCKED = 0x0040
    MCP9808_REG_CONFIG_INTCLR = 0x0020
    MCP9808_REG_CONFIG_ALERTSTAT = 0x0010
    MCP9808_REG_CONFIG_ALERTCTRL = 0x0008
    MCP9808_REG_CONFIG_ALERTSEL = 0x0002
    MCP9808_REG_CONFIG_ALERTPOL = 0x0002
    MCP9808_REG_CONFIG_ALERTMODE = 0x0001
    MCP9808_REG_CONFIG = 0x01
    MCP9808_REG_UPPER_TEMP = 0x02
    MCP9808_REG_LOWER_TEMP = 0x03
    MCP9808_REG_CRIT_TEMP = 0x04
    MCP9808_REG_AMBIENT_TEMP = 0x05
    MCP9808_REG_MANUF_ID = 0x06
    MCP9808_REG_DEVICE_ID = 0x07

    def __init__(self, *args, **kwargs):
        super(Mcp9808Module, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))
        # Assert it's the right thing
        mid = self._data.readU16(self.MCP9808_REG_MANUF_ID, False)
        if mid != 0x0054:
            self._log.error('Not right manufacturer (0x54): %s' % mid)
        did = self._data.readU16(self.MCP9808_REG_DEVICE_ID, False)
        if did != 0x0400:
            self._log.error('Not right device ID (0x4): %s' % did)

    def get_temperature(self):
        data = self._data.readU16(self.MCP9808_REG_AMBIENT_TEMP, False)
        temperature = data & 0x0FFF
        temperature /= 16.0
        if data & 0x1000:
            temperature -= 256
        return temperature

    def read_data(self):
        """
        Get the temperature readings.
        """
        temp_time_start = self._get_time()
        try:
            temperature = self.get_temperature()
        except IOError:
            temperature = None
        temp_time_stop = self._get_time()
        temp_time_delta = temp_time_stop - temp_time_start
        data = [
            (self._name, 'temperature', temperature, temp_time_delta),
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
            }
        }
