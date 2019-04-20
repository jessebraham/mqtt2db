#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging

from mqtt2pg.config import load_config
from mqtt2pg.subscriber import MQTTSubscriber


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    config = load_config()
    mqtt_config = config.get("mqtt", {})
    pg_config = config.get("pg", {})

    topics_and_handlers = {}

    try:
        mqttc = MQTTSubscriber(mqtt_config, pg_config, topics_and_handlers)
        mqttc.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, shutting down")
    except Exception as exc:
        logger.critical(f"Fatal: {exc}")
