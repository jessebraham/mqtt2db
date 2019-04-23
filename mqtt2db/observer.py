# -*- encoding: utf-8 -*-

import datetime
import logging
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from mqtt2db.config import load_config


logger = logging.getLogger(__name__)


class FileChangedHandler(FileSystemEventHandler):
    """
    Watch for a specific file to change, in this case our configuration file,
    and re-configure and restart the client when this event occurs.
    """

    def __init__(self, client, filename, wait=1):
        self.client = client
        self.filename = filename
        self.last_change = datetime.datetime.min
        self.wait = wait

    def on_modified(self, event):
        """
        When a 'modified' event is received, start by checking the file name
        which triggered the event; if it does not match our config file's name,
        ignore the event. To avoid excessive reloading, also ignore the event
        if the last change time was less than the configured number of seconsd.

        Attempt to load the new configuration, logging an error and simply
        returning if the configuration cannot be loaded.

        Upon the successful loading of our new configuration, re-configure and
        restart our client.
        """
        (_, filename) = os.path.split(event.src_path)
        if filename != self.filename:
            return

        if (datetime.datetime.now() - self.last_change).seconds < self.wait:
            return

        config = load_config()
        if not config["_meta"]["success"]:
            logger.info("Reloading configuration failed, ignoring")
            return

        self.client.configure(config)
        self.client.restart()
        self.last_change = datetime.datetime.now()


def create_observer(client, filepath):
    """
    Create a new Observer which watches for changes to the specified config
    file.
    """
    (path, filename) = os.path.split(filepath)
    handler = FileChangedHandler(client, filename)

    observer = Observer()
    observer.schedule(handler, path)

    return observer
