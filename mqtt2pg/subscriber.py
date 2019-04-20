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
        """
        The `config` dict MUST have "mqtt" and "postgresql" keys in order for
        this class to operate properly. In turn, those keys respective dicts
        must contain all required configuration for our MQTT Broker and
        PostgreSQL. Refer to `template.config.toml` for all required fields.

        If provided, the dict referenced by the "topics" key should contains
        string-class key-value pairs. All handler classes should inherit from
        `handlers.BaseMessageHandler`.
        """
        super().__init__()
        self.enable_logger(logger)
        self.mqtt_config = config.get("mqtt", {})
        self.pg_config = config.get("postgresql", {})
        self.qos = qos
        self.topics_and_handlers = config.get("topics", {})

    def run(self):
        """
        Establish connections with both our MQTT Broker and PostgreSQL, and
        start the MQTT client's event loop.
        """
        self.conn = psycopg2.connect(**self.pg_config)
        self.connect(**self.mqtt_config)
        self.loop_forever()

    # -------------------------------------------------------------------------
    # Event Handlers

    def on_connect(self, client, userdata, flags, rc):
        """
        Upon establishing a connection to our MQTT Broker, for each topic pair
        within the `topics_and_handlers` dict's key list, subscribe to the
        topic with the class-configured QOS level.
        """
        for topic in self.topics_and_handlers.keys():
            self.subscribe(topic, self.qos)

    def on_message(self, client, userdata, msg):
        """
        When a message is received on any of our subscribed topics, attempt
        to look up the appropriate message handler class, and invoke its
        `process` function with the provided message.
        """
        try:
            handler = self.topics_and_handlers[msg.topic]
            handler.process(self.conn, msg)
        except KeyError as exc:
            logger.exception(exc)
