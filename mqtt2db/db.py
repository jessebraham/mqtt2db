# -*- encoding: utf-8 -*-

import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import MetaData, Table


logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    TODO: document me
    TODO: better error handling
    """

    def __init__(self, config):
        self.engine = create_engine(self.conn_string(config))
        self.metadata = MetaData()

    @staticmethod
    def conn_string(config):
        # Make a copy of the 'database' dict to avoid popping the value from
        # the original 'config' dict.
        db_config = dict(config)
        drivername = db_config.pop("drivername")
        return url.URL(drivername, **db_config)

    def connect(self):
        self.conn = self.engine.connect()

    def reload(self, config):
        self.engine = create_engine(self.conn_string(config))
        self.connect()
    def reflect_table(self, table):
        try:
            table = Table(
                table, self.metadata, autoload=True, autoload_with=self.engine
            )
        except NoSuchTableError as exc:
            logger.exception(exc)
            table = None

        return table

    def insert_data(self, table, data):
        row = table.insert().values(**data)
        self.engine.execute(row)
