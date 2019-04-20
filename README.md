# mqtt2pg

[![Build Status](https://travis-ci.org/jessebraham/mqtt2pg.svg?branch=master)](https://travis-ci.org/jessebraham/mqtt2pg) [![Coverage Status](https://coveralls.io/repos/github/jessebraham/mqtt2pg/badge.svg?branch=master)](https://coveralls.io/github/jessebraham/mqtt2pg?branch=master)

**mqtt2pg** is a simple service written in [Python](https://www.python.org/) which subscribes to any number of configured topics on an MQTT broker and stores each received message in PostgreSQL.

It is required that you have both an MQTT Broker (eg. [Mosquitto](https://mosquitto.org/)) and a [PostgreSQL]() server. Currently, automatic table creation is not handled; databases and tables **must** be present in order for this application to operate properly. This may or may not change in the future.

If desired, custom message handlers can be defined and configured for added flexibility. See the [Message Handlers](#message-handlers) section for more information.

- - -

**mqtt2pg** is made possible by the following packages:  
[paho-mqtt](https://github.com/eclipse/paho.mqtt.python/) | [psycopg2-binary](https://github.com/psycopg/psycopg2) | [toml](https://github.com/uiri/toml)

Development and testing aided by:  
[black](https://github.com/ambv/black) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

- - -

## Getting Started

**mqtt2pg** requires **Python 3.6** or higher. It's recommended to use a virtual environment.

Begin by cloning the repository and installing all required Python packages:

```bash
$ git clone https://github.com/jessebraham/mqtt2pg.git
$ cd mqtt2pg
$ pip install -r requirements.txt
```

A `config.toml` file **must** be present within the project directory. Copy the template and edit the new configuration file. More information on configuration can be found in the [Configuration](#configuration) section.

```bash
$ cp template.config.toml config.toml
$ # edit config.toml using your favorite text editor
```

Finally, run the application:

```bash
$ python -m mqtt2pg.main
```

## Configuration

TODO: document me

## Message Handlers

TODO: document me
