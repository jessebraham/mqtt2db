# -*- encoding: utf-8 -*-

from abc import ABC, abstractmethod


class BaseMessageHandler(ABC):
    """
    Abstract base class for defining MQTT message handlers. Inheriting classes
    MUST implement the `process` function, as it is invoked directly.

    Additionally includes a small number of simple helper functions for use
    by inheriting classes.
    """

    @classmethod
    @abstractmethod
    def process(cls, db, message):
        raise NotImplementedError()

    @staticmethod
    def keys_match_columns(table, data):
        columns = [c.name for c in table.columns]
        return set(data.keys()) == set(columns)
