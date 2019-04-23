# mqtt2db

[![Build Status](https://travis-ci.org/jessebraham/mqtt2db.svg?branch=master)](https://travis-ci.org/jessebraham/mqtt2db) [![Coverage Status](https://coveralls.io/repos/github/jessebraham/mqtt2db/badge.svg?branch=master)](https://coveralls.io/github/jessebraham/mqtt2db?branch=master)

**mqtt2db** is a simple service written in [Python](https://www.python.org/) which subscribes to any number of configured topics on an MQTT broker and stores each received message in PostgreSQL.

It is required that you have both an MQTT Broker (eg. [Mosquitto](https://mosquitto.org/), [VerneMQ](https://github.com/vernemq/vernemq), [HBMQTT](https://github.com/beerfactory/hbmqtt), etc.) and a [PostgreSQL]() server. Currently, automatic table creation is not supported; databases and tables **must** be present in order for this application to operate properly. The keys in your JSON data must match exactly the names of the columns in the table, and the table's name must exactly match that of the topic. This all may or may not change in the future.

If desired, custom message handlers can be defined and configured for added flexibility. See the [Message Handlers](#message-handlers) section for more information.

- - -

**mqtt2db** is made possible by the following packages:  
[paho-mqtt](https://github.com/eclipse/paho.mqtt.python/) | [psycopg2-binary](https://github.com/psycopg/psycopg2) | [toml](https://github.com/uiri/toml) | [watchdog](https://github.com/gorakhargosh/watchdog)

Development and testing aided by:  
[black](https://github.com/ambv/black) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

- - -

## Quickstart

**mqtt2db** requires **Python 3.6** or higher. It's recommended to use a virtual environment.

Begin by cloning the repository and installing all required Python packages:

```bash
$ git clone https://github.com/jessebraham/mqtt2db.git
$ cd mqtt2db
$ pip install -r requirements.txt
```

A `config.toml` file **must** be present within the project directory. Copy the template and edit the new configuration file. More information on configuration can be found in the [Configuration](#configuration) section.

```bash
$ cp template.config.toml config.toml
$ # edit config.toml using your favorite text editor
```

Finally, run the application:

```bash
$ python -m mqtt2db.main
```

## Configuration

TODO: document me

## Message Handlers

TODO: document me
