#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging
import sys

from mqtt2db.config import load_config
from mqtt2db.subscriber import Subscriber


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    config = load_config()
    if not config["meta"]["success"]:
        logger.error("A valid configuration file could not be loaded")
        sys.exit(1)

    try:
        client = Subscriber(config)
        client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, shutting down")
        client.stop()
    except Exception as exc:
        logger.exception(exc)
