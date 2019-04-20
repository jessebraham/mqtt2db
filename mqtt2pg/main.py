#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging

from mqtt2pg.config import load_config
from mqtt2pg.handlers import DefaultMessageHandler
from mqtt2pg.subscriber import Subscriber


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Begin by loading the contents of the confiuguration file, attempting to
    # parse the TOML to a dict. This will also construct the dict of topics
    # and handlers if any such configuration has been provided.
    config = load_config(default_handler=DefaultMessageHandler)

    # Instantiate the Subscriber class using the above configuration, and
    # run our client. Log any exceptions that may occur, and exit when a
    # keyboard interrupt (Ctrl-c) has been received.
    try:
        client = Subscriber(config)
        client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, shutting down")
    except Exception as exc:
        logger.exception(exc)
