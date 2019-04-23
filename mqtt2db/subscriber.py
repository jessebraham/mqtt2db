# -*- encoding: utf-8 -*-

import logging

import paho.mqtt.client as mqtt
import psycopg2


logger = logging.getLogger(__name__)


class Subscriber(mqtt.Client):
    """
    Connects to an MQTT Broker and subscribes to all configured topics,
    registering the appropriate `on_message` handlers for each topic in the
    process.
    """

    def __init__(self, config, qos=0):
        super().__init__()
        self.enable_logger(logger)
        self.configure(config)
        self.qos = qos

    def configure(self, config):
        """
        The 'config' dict requires that two keys are present: "mqtt" and
        "postgresql". Optionally a third key, "topics", may be provided.

        "mqtt" contains the information required to connect to our MQTT broker.

        "postgresql" contains the information required to connect to our
        database server, including authentication and which database to store
        our data in.

        "topics" contains a list of key-value pairs, with the key being the
        topic to subsribe to on the MQTT broker, and the value being the
        message handler to use. If no handler is provided, the default is used.

        Refer to `template.config.toml` to see an sample configuration.
        """
        self.mqtt_config = config.get("mqtt", {})
        self.pg_config = config.get("postgresql", {})
        self.topics_and_handlers = config.get("topics", {})

    def run(self):
        """
        Establish connections with our MQTT broker and PostgreSQL server, and
        start the MQTT client's event loop.
        """
        self.conn = psycopg2.connect(**self.pg_config)
        self.connect(**self.mqtt_config)
        self.loop_forever()

    def restart(self):
        """
        Close the connections with our MQTT broker and PostgreSQL server, and
        call the `run` method to re-establish both connections and restart the
        event loop.
        """
        self.conn.close()
        self.conn = psycopg2.connect(**self.pg_config)
        self.reconnect()

    # -------------------------------------------------------------------------
    # Event Handlers

    def on_connect(self, client, userdata, flags, rc):
        """
        When a connection with our MQTT broker has been established, iterate
        through all configured topics and subscribe to each using the class-
        configured QOS level.
        """
        for topic in self.topics_and_handlers.keys():
            self.subscribe(topic, self.qos)

    def on_message(self, client, userdata, msg):
        """
        Upon receiving a new message, attempt to look up the appropriate
        message handler, and on success call its `process` method on the
        message. Log any exceptions, along with the message, if they occur.
        """
        try:
            handler = self.topics_and_handlers[msg.topic]
            handler.process(self.conn, msg)
        except KeyError as exc:
            logger.exception(exc)
            logger.error(f"Topic: {msg.topic}")
            logger.error(f"Payload: {msg.payload}")
