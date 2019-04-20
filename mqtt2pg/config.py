#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os

import toml


def load_config(filename="config.toml"):
    if not os.path.isfile(filename):
        return {}

    try:
        config = toml.load(filename)
    except (TypeError, toml.decoder.TomlDecodeError):
        config = {}

    return config
