#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging

from mqtt2pg.config import load_config
from mqtt2pg.handlers import DefaultMessageHandler
from mqtt2pg.subscriber import Subscriber


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    topics_and_handlers = {"default": DefaultMessageHandler}

    try:
        config = load_config()
        client = Subscriber(config, topics_and_handlers)
        client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, shutting down")
    except Exception as exc:
        logger.critical(f"Fatal: {exc}")
