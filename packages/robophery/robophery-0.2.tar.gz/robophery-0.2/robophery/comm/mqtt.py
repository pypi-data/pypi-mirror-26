import json


class MqttComm(object):
    """
    Base class for implementing MQTT communication.
    """

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name')
        self._manager = kwargs.get('manager', None)
        self._class = kwargs.get('class', None)
        self._host = kwargs.get('host', '127.0.0.1')
        self._port = kwargs.get('port', 1883)
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)
        self._subscribe_topic = kwargs.get(
            'subscribe_topic', 'robophery_sub/{0}'.format(self._manager._name))
        self._publish_topic = kwargs.get(
            'publish_topic', 'robophery_pub/{0}'.format(self._manager._name))
        self._publish_format = kwargs.get('publish_format', 'SenML')
        self._log = self._manager._get_logger(self._name)
        self._log.info("Started communication channel {0}.".format(self))

    def __str__(self):
        if self._username is None:
            return "{0} (connected to tcp://{1}:{2}, publishing to {3} in {4} format, subscribed to {5})".format(self._base_name(), self._host, self._port, self._publish_topic, self._publish_format, self._subscribe_topic)
        else:
            return "{0} (connected to tcp://{1}:{2}, publishing to {3} in {4} format, subscribed to {5}, user {6})".format(self._base_name(), self._host, self._port, self._publish_topic, self._publish_format, self._subscribe_topic, self._username)

    def _base_name(self):
        return '{0} {1}'.format(self._class.split('.')[-1], self._name)

    def _to_string(self, datum):
        return json.dumps(datum)

    def receive_data(self, topic, raw_data):
        try:
            data = json.loads(raw_data)
        except Exception as e:
            self._log.error("Error parsing received message {0}: {1}".format(raw_data, e))
            return
        tgt = data.get('tgt', 'unknown')
        fun = data.get('fun', 'get_data')
        arg = data.get('arg', None)
        if tgt in self._manager._module:
            output = self._manager._module[tgt].commit_action(fun, arg)
        else:
            output = ""
        return output

    def send_data(self, data):
        for name, datum in data.items():
            self.send_datum({name: datum})

    def send_datum(self, datum):
        raise NotImplementedError
