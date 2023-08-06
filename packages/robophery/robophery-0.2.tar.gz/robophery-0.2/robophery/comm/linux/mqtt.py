import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from robophery.comm.mqtt import MqttComm


class PahoMqttComm(MqttComm):

    def __init__(self, *args, **kwargs):
        super(PahoMqttComm, self).__init__(*args, **kwargs)
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        if self._username is not None:
            self._client.username_pw_set(
                self._username, password=self._password)
        self._client.connect(self._host, self._port, 60)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from
        the server.
        """
        self._log.info("Connected to {0}:{1} with result code {2}.".format(
            self._host, self._port, rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("{0}".format(self._subscribe_topic))

    def _on_message(self, client, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the broker.
        """
        self._log.debug("Received message {0} on topic {1}". format(
            msg.payload, msg.topic))
        self.receive_data(msg.topic, msg.payload)

    def send_data(self, data):
        final_data = {}
        for name, datum in data.items():
            names = name.split('.')
            if 'avg_value' in datum:
                if names[0] in final_data:
                    final_data[names[0]][names[1]] = datum['avg_value']
                else:
                    final_data[names[0]] = {names[1]: datum['avg_value']}
        for name, datum in final_data.items():
            topic = "{0}/{1}".format(self._publish_topic, name)
            if self._username is not None:
                auth = {
                    'username': self._username,
                    'password': self._password
                }
            else:
                auth = None
            publish.single(topic,
                           payload=self._to_string(datum),
                           hostname=self._host,
                           client_id=self._manager._name,
                           auth=auth,
                           # tls=tls,
                           port=self._port,
                           protocol=mqtt.MQTTv311)
            self._log.debug(
                "Published message {0} to {1}/{2}.".format(datum, self._host, topic))
