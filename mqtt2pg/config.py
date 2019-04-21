# -*- encoding: utf-8 -*-

import logging
import os

import toml

from toml.decoder import TomlDecodeError

import mqtt2pg.handlers as handlers


logger = logging.getLogger(__name__)


def load_config(filename="config/config.toml"):
    """
    Provided with a path to a configuration file, attempt to parse its TOML
    contents into a dict, returning the results.
    """
    filepath = os.path.abspath(filename)
    try:
        config = toml.load(filepath)
    except (FileNotFoundError, IsADirectoryError, TomlDecodeError, TypeError) as exc:
        logger.exception(exc)
        config = {}

    if "topics" in config:
        config["topics"] = load_topics_and_handlers(config)

    config = add_meta(config, filepath)
    return config


def add_meta(config, filepath):
    """
    Create a dict in 'config' under the key "_meta" containing the absolute
    path to the specified configuration file, as well as whether or not the
    file was loaded successfully and formatted properly.
    """
    config["_meta"] = {
        "filepath": filepath,
        "success": all(key in config for key in ("mqtt", "postgresql")),
    }
    return config


def load_topics_and_handlers(config):
    """
    Provided with a configuration dict, attempt to extract the "topics" dict.

    Iterate through the key-value pairs of "topics", attempting to load a
    handler class if specified, and assigning the DefaultMessageHandler in the
    case that one is not.
    """
    topics = config.get("topics")
    topics_and_handlers = {}

    for topic, handler in topics.items():
        topics_and_handlers[topic] = try_load_handler(handler)

    return topics_and_handlers


def try_load_handler(handlername):
    """
    Provided with the name of a message handler class, attempt to load that
    class, returning it upon success.

    If the class does not exist, or if it does not subtype the
    `BaseMessageHandler` class, we will instead return the
    DefaultMessageHandler.
    """
    try:
        handler = getattr(handlers, handlername)
        assert issubclass(handler, handlers.BaseMessageHandler)
    except (AssertionError, AttributeError):
        handler = handlers.DefaultMessageHandler

    return handler
