# -*- encoding: utf-8 -*-

import logging

import toml

from toml.decoder import TomlDecodeError

import mqtt2pg.handlers as handlers


logger = logging.getLogger(__name__)


def load_config(filename="config.toml", default_handler=None):
    """
    Given a path to a configuration file, attempt to read its contents and
    parse out the TOML to a dict, returning the results or an empty dict on
    failure.
    """
    try:
        config = toml.load(filename)
    except (FileNotFoundError, TomlDecodeError, TypeError) as exc:
        logger.exception(exc)
        config = {}

    if "topics" in config:
        if default_handler is not None:
            config["topics"] = extract_topic_handlers(config, default_handler)
        else:
            config.pop("topics")

    return config


def extract_topic_handlers(config, default_handler):
    """
    Provided with a configuration dict, attempt to extract the "topics" dict.

    Iterate through the key-value pairs in "topics", attempting to load a
    handler class if specified, and assigning the provided default handler in
    the case that one is not.
    """
    topics = config.get("topics", {})
    topics_and_handlers = {}

    for topic, handler in topics.items():
        if handler:
            handler = try_load_handler(handler)
        topics_and_handlers[topic] = handler if handler else default_handler

    return topics_and_handlers


def try_load_handler(handlername):
    """
    Provided with the name of a message handler class, attempt to load that
    class, returning it upon success.

    If the class does not exist, or if it does not subtype the
    `BaseMessageHandler` class, we will instead return `None` to indicate that
    the class loading was not successful.
    """
    try:
        handler = getattr(handlers, handlername)
        assert issubclass(handler, handlers.BaseMessageHandler)
    except (AssertionError, AttributeError) as exc:
        logger.exception(exc)
        handler = None

    return handler
