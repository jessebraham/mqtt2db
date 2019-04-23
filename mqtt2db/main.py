#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import logging
import sys

from mqtt2db.config import load_config
from mqtt2db.observer import create_observer
from mqtt2db.subscriber import Subscriber


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Begin by loading the contents of the confiuguration file, attempting to
    # parse the TOML to a dict. This will also construct the dict of topics
    # and handlers if any such configuration has been provided.
    config = load_config()
    meta = config.get("_meta")

    # If the meta-config's `success` attribute is set to False, then a valid
    # configuration file could not be loaded. In this case, we must terminate.
    if not meta["success"]:
        logger.error("A valid configuration file could not be loaded.")
        sys.exit(1)

    # Instatiate both the filesystem observer and our Subscriber classes using
    # the above configuration. Start the observer and client, logging any
    # exceptions that may occur in the process. If a keyboard interrupt
    # (Ctrl-c) is received, gracefully shut down.
    try:
        client = Subscriber(config)
        observer = create_observer(client, meta["filepath"])

        observer.start()
        client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, shutting down")
        observer.stop()
        observer.join()
    except Exception as exc:
        logger.exception(exc)
