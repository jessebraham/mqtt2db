# -*- encoding: utf-8 -*-

import logging

import paho.mqtt.client as mqtt
import psycopg2


logger = logging.getLogger(__name__)


class MQTTSubscriber(mqtt.Client):
    """
    This subscriber assumes that ingress data is in JSON format. This may
    change or become configurable in the future.
    """

    def __init__(self, mqtt_config, pg_config, topics_and_handlers, qos=0):
        super().__init__()
        self.conn = psycopg2.connect(**pg_config)
        self.mqtt_config = mqtt_config
        self.topics_and_handlers = topics_and_handlers
        self.qos = qos

    def on_log(self, mqttc, obj, level, message):
        """
        TODO: try to map `level` to an actual string, log at proper level (if
              that's even how this works...)
        """
        logger.info(message)

    def on_connect(self, mqttc, obj, flags, rc):
        for topic in self.topics_and_handlers.keys():
            self.subscribe(topic, self.qos)

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.info(f"Subscribed: {mid} {granted_qos}")

    def on_message(self, mqttc, obj, msg):
        try:
            handler = self.topics_and_handlers[msg.topic]
            handler.process(self.conn, msg)
        except KeyError as exc:
            logger.error(exc)

    def run(self):
        self.connect(**self.mqtt_config)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
