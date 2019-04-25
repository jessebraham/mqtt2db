# -*- encoding: utf-8 -*-

import datetime
import logging
import os

import paho.mqtt.client as mqtt

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from mqtt2db.config import load_config
from mqtt2db.db import ConnectionManager


logger = logging.getLogger(__name__)


class Subscriber(mqtt.Client):
    def __init__(self, config, qos=0):
        super().__init__()
        self.configure(config)
        self.enable_logger(logger)
        self.db = ConnectionManager(self.db_config)
        self.observer = self.create_observer(config)
        self.qos = qos

    def configure(self, config):
        self.config = config
        self.db_config = config.get("database", {})
        self.mqtt_config = config.get("mqtt", {})
        self.topics_and_handlers = config.get("topics", {})

    def create_observer(self, config):
        handler = FileChangedHandler(config, self.reload)

        observer = Observer()
        observer.schedule(handler, os.path.dirname(config["filepath"]))
        observer.start()

        return observer

    def run(self):
        self.db.connect()
        self.connect(**self.mqtt_config)
        self.loop_forever()

    def reload(self, config):
        logger.info("Configuration changes detected, reloading")
        self.configure(config)
        self.db.reload(self.db_config)
        self.connect(**self.mqtt_config)

    def stop(self):
        self.disconnect()
        self.observer.stop()
        self.observer.join()

    # -------------------------------------------------------------------------
    # Event Handlers

    def on_connect(self, client, userdata, flags, rc):
        for topic in self.topics_and_handlers.keys():
            self.subscribe(topic, self.qos)

    def on_message(self, client, userdata, msg):
        try:
            handler = self.topics_and_handlers[msg.topic]
            handler.process(self.db, msg)
        except KeyError as exc:
            logger.exception(exc)
            logger.error(f"Topic: {msg.topic}")
            logger.error(f"Payload: {msg.payload}")


class FileChangedHandler(FileSystemEventHandler):
    def __init__(self, config, callback, wait=1):
        self.callback = callback
        self.filename = os.path.basename(config["filepath"])
        self.last_change = datetime.datetime.min
        self.wait = wait

    def on_modified(self, event):
        if os.path.basename(event.src_path) != self.filename:
            return

        if (datetime.datetime.now() - self.last_change).seconds < self.wait:
            return

        config = load_config(event.src_path)
        if not config["success"]:
            logger.info("Reloading configuration failed, ignoring changes")
            return

        self.last_change = datetime.datetime.now()
        self.callback(config)
