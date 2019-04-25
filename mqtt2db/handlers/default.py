# -*- encoding: utf-8 -*-

import json
import logging

from .base import BaseMessageHandler


logger = logging.getLogger(__name__)


class DefaultMessageHandler(BaseMessageHandler):
    """
    Insert the payload of the message verbatim into the table with its name
    matching that of the originating topic. It is assumed that the message's
    payload is in JSON format, and that each key corresponds to a column.

    If the keys do not match the column names, a ValueError is raised.
    """

    @classmethod
    def process(cls, db, message):
        table = db.reflect_table(message.topic)
        data = json.loads(message.payload)

        if not cls.keys_match_columns(table, data):
            logger.error(
                f"Data key(s) did not match schema for topic '{message.topic}'"
            )
            return

        db.insert_data(table, data)


BaseMessageHandler.register(DefaultMessageHandler)
