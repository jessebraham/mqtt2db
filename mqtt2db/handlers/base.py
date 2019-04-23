# -*- encoding: utf-8 -*-

from abc import ABC, abstractmethod

from psycopg2 import sql


class BaseMessageHandler(ABC):
    """
    Abstract base class for defining MQTT message handlers. Inheriting classes
    MUST implement the `process` function, as it is invoked directly.

    Additionally includes a small number of simple helper functions for use
    by inheriting classes.
    """

    @classmethod
    @abstractmethod
    def process(cls, conn, message):
        raise NotImplementedError()

    @classmethod
    def keys_match_columns(cls, cursor, table, data):
        keys = [key.lower() for key in data.keys()]
        columns = cls.select_column_names(cursor, table)
        return set(keys) == set(columns)

    @staticmethod
    def select_column_names(cursor, table):
        cursor.execute(
            sql.SQL("SELECT * FROM {} LIMIT 0").format(sql.Identifier(table))
        )
        column_names = [desc[0].lower() for desc in cursor.description]
        return column_names

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
