import Adafruit_DHT
from robophery.interface.gpio import GpioModule


class Dht22Module(GpioModule):
    """
    Module for DHT22 temperature and humidity sensor.
    """
    DEVICE_NAME = 'dht22'

    def __init__(self, *args, **kwargs):
        super(Dht22Module, self).__init__(*args, **kwargs)
        self._pin = kwargs.get('data').get('pin')
        self._type = 22

    def commit_action(self, action):
        if action == 'read_data':
            return self.read_data()

    def read_data(self):
        """
        Query DHT22 to get the humidity and temperature readings.
        """
        read_time_start = self._get_time()
        humidity, temperature = Adafruit_DHT.read(self._type, self._pin)
        read_time_stop = self._get_time()
        read_time_delta = (read_time_stop - read_time_start) / 2
        if temperature is None or humidity is None:
            self._log.error("Data CRC failed while reading data.")
            data = [
                (self._name, 'temperature', None, read_time_delta),
                (self._name, 'humidity', None, read_time_delta)
            ]
        else:
            if humidity > 0 and humidity < 100:
                data = [
                    (self._name, 'temperature', temperature, read_time_delta),
                    (self._name, 'humidity', humidity, read_time_delta)
                ]
            else:
                self._log.error('Humidity out of range')
                data = [
                    (self._name, 'temperature', None, read_time_delta),
                    (self._name, 'humidity', None, read_time_delta)
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
                'precision': 0.5,
                'range_low': -40,
                'range_high': 80,
                'sensor': self.DEVICE_NAME
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'precision': 5,
                'range_low': 0,
                'range_high': 100,
                'sensor': self.DEVICE_NAME
            }
        }
