# -*- encoding: utf-8 -*-

from abc import ABC, abstractmethod

from psycopg2 import sql


class BaseMessageHandler(ABC):
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
