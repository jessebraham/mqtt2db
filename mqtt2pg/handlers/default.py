# -*- encoding: utf-8 -*-

import json
import logging

from psycopg2 import sql

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
    def process(cls, conn, message):
        cursor = conn.cursor()
        data = json.loads(message.payload)

        match = cls.keys_match_columns(cursor, message.topic, data)
        if not match:
            logger.error("Data key(s) did not match schema for topic")
            raise ValueError()

        cls.insert(cursor, message.topic, data)
        conn.commit()

    @staticmethod
    def insert(cursor, table, data):
        cursor.execute(
            sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(", ").join(map(sql.Identifier, data.keys())),
                sql.SQL(", ").join(map(sql.Placeholder, data.keys())),
            ),
            data,
        )
