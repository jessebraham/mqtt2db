# -*- encoding: utf-8 -*-

from mqtt2db.config import load_config, load_topics_and_handlers, try_load_handler
from mqtt2db.handlers import BaseMessageHandler, DefaultMessageHandler


CONFIGURATION = """
[mqtt]
host = "localhost"
port = 1883
keepalive = 60

[database]
drivername = "postgresql"
host = "localhost"
port = 5432
database = "mqtt2db"
username = "postgres"
password = "postgres"

[topics]
environment = ""
"""


def test_load_config(tmpdir):
    f = tmpdir / "config.toml"
    f.write_text(CONFIGURATION, encoding="utf-8")

    config = load_config(filename=str(f))
    assert isinstance(config, dict)
    assert "mqtt" in config.keys()
    assert "database" in config.keys()
    assert "topics" in config.keys()

    nofile_config = load_config(filename="")
    assert isinstance(nofile_config, dict)
    assert len(nofile_config.keys()) >= 2


def test_extract_topic_handlers():
    config = {"topics": {"default": "", "updates": "DefaultMessageHandler"}}

    topics_and_handlers = load_topics_and_handlers(config)
    assert isinstance(topics_and_handlers, dict)

    assert "default" in topics_and_handlers
    assert issubclass(topics_and_handlers["default"], DefaultMessageHandler)

    assert "updates" in topics_and_handlers
    assert issubclass(topics_and_handlers["updates"], DefaultMessageHandler)


def test_try_load_handler():
    handler = try_load_handler("DefaultMessageHandler")
    assert issubclass(handler, BaseMessageHandler)
    assert issubclass(handler, DefaultMessageHandler)

    invalid_handler = try_load_handler("InvalidMessageHandler")
    assert issubclass(invalid_handler, DefaultMessageHandler)

    no_handler = try_load_handler("")
    assert issubclass(no_handler, DefaultMessageHandler)
