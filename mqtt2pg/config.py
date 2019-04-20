# -*- encoding: utf-8 -*-

import logging

import toml

from toml.decoder import TomlDecodeError

import mqtt2pg.handlers


logger = logging.getLogger(__name__)


def load_config(filename="config.toml"):
    try:
        config = toml.load(filename)
    except (FileNotFoundError, TomlDecodeError, TypeError) as exc:
        logger.exception(exc)
        config = {}

    return config


def extract_topic_handlers(config, default_handler):
    topics = config.get("topics", {})
    topics_and_handlers = {}

    for topic, handler in topics.items():
        # If a handler was provided, we first attempt to load that class. If
        # no handler was provided, or the provided handler could not be loaded,
        # we assign the default handler to the topic, otherwise we set the
        # loaded class as the handler.
        if handler:
            handler = load_handler(handler)
        topics_and_handlers[topic] = handler if handler else default_handler

    return topics_and_handlers


def load_handler(handlername):
    try:
        handler = getattr(mqtt2pg.handlers, handlername)
    except NameError as exc:
        logger.exception(exc)
        handler = None

    return handler
