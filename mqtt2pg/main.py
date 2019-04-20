#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging

from mqtt2pg.config import extract_topic_handlers, load_config
from mqtt2pg.handlers import DefaultMessageHandler
from mqtt2pg.subscriber import Subscriber


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    config = load_config()
    topics_and_handlers = extract_topic_handlers(
        config, default_handler=DefaultMessageHandler
    )

    try:
        client = Subscriber(config, topics_and_handlers)
        client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, shutting down")
    except Exception as exc:
        logger.exception(exc)
