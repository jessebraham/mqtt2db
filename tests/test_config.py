# -*- encoding: utf-8 -*-

from mqtt2pg.config import load_config, extract_topic_handlers, try_load_handler
from mqtt2pg.handlers import BaseMessageHandler, DefaultMessageHandler


CONFIGURATION = """
[mqtt]
host = "localhost"
port = 1883
keepalive = 60

[pg]
host = "localhost"
port = 5432
dbname = "mqtt2pg"
user = "postgres"
password = "postgres"

[topics]
environment = ""
"""


def test_load_config(tmpdir):
    f = tmpdir / "config.toml"
    f.write_text(CONFIGURATION, encoding="utf-8")

    config = load_config(filename=str(f))
    assert isinstance(config, dict)
    assert len(config.keys()) > 0
    assert "topics" not in config.keys()

    config_w_default = load_config(
        filename=str(f), default_handler=DefaultMessageHandler
    )
    assert "mqtt" in config_w_default.keys()
    assert "pg" in config_w_default.keys()
    assert "topics" in config_w_default.keys()

    nofile_config = load_config(filename="")
    assert isinstance(nofile_config, dict)
    assert len(nofile_config.keys()) == 0


def test_extract_topic_handlers():
    config = {"topics": {"default": "", "updates": "DefaultMessageHandler"}}

    topics_and_handlers = extract_topic_handlers(config, DefaultMessageHandler)

    assert isinstance(topics_and_handlers, dict)
    assert "default" in topics_and_handlers
    assert issubclass(topics_and_handlers["default"], DefaultMessageHandler)
    assert "updates" in topics_and_handlers
    assert issubclass(topics_and_handlers["updates"], DefaultMessageHandler)


def test_try_load_handler():
    handler = try_load_handler("DefaultMessageHandler")
    assert issubclass(handler, BaseMessageHandler)

    invalid_handler = try_load_handler("InvalidMessageHandler")
    assert invalid_handler is None

    no_handler = try_load_handler("")
    assert no_handler is None
