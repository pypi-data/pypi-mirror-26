# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import colorlog
import logging
import os
from multiprocessing import Lock, Manager
import signal


class Context(object):
    """
    Stores settings across multiple independent processing units

    This is a key-value store, that supports concurrency
    across multiple processes.

    """

    def __init__(self, settings=None, filter=None):
        """
        Stores settings across multiple independent processing units

        :param settings: the set of variables managed in this context
        :type settings: dict

        :param filter: a function to interpret values on check()
        :type filter: callable

        """

        # prevent Manager() process to be interrupted
        handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

        self.lock = Lock()
        self.values = Manager().dict()

        # restore current handler for the rest of the program
        signal.signal(signal.SIGINT, handler)

        self.filter = filter if filter else self._filter

        if settings:
            self.apply(settings)

    def apply(self, settings={}):
        """
        Applies multiple settings at once

        :param settings: variables to be added to this context
        :type settings: dict

        """
        with self.lock:

            for key in settings.keys():
                if isinstance(settings[key], dict):
                    for label in settings[key].keys():
                        self.values[key+'.'+label] = settings[key].get(label)
                else:
                    self.values[key] = settings[key]

    def clear(self):
        """
        Clears content of a context
        """
        with self.lock:
            self.values.clear()

    @property
    def is_empty(self):
        """
        Does the context store something?

        :return: True if there at least one value, False otherwise
        """
        with self.lock:
            return len(self.values.keys()) < 1

    def check(self,
              key,
              default=None,
              is_mandatory=False,
              validate=None,
              filter=False):
        """
        Checks some settings

        :param key: the key that has to be checked
        :type primary: str

        :param default: the default value if no statement can be found
        :type default: str

        :param is_mandatory: raise an exception if keys are not found
        :type is_mandatory: bool

        :param validate: a function called to validate values before the import
        :type validate: callable

        :param filter: look at the content, and change it eventually
        :type filter: bool

        Example::

            context = Context({
                'spark': {
                    'room': 'My preferred room',
                    'participants':
                        ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                    'team': 'Anchor team',
                    'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY>',
                    'webhook': "http://73a1e282.ngrok.io",
                    'weird_token', '$WEIRD_TOKEN',
                }
            })

            context.check('spark.room', is_mandatory=True)
            context.check('spark.team')
            context.check('spark.weird_token', filter=True)

        When a default value is provided, it is used to initialize
        properly a missing key::

            context.check('general.switch', 'on')

        Another usage is to ensure that a key has been set::

            context.check('spark.room', is_mandatory=True)

        Additional control can be added with the validation function::

            context.check('general.switch',
                          validate=lambda x: x in ('on', 'off'))

        When filter is True, if the value is a string starting with '$',
        then a variable with the same name is loaded from the environment::

            >>>token=context.check('spark.weird_token', filter=True)
            >>>assert token == os.environ.get('WEIRD_TOKEN')
            True

        The default filter can be changed at the creation of a context::

            >>>context=Context(filter=lambda x : x + '...')

        This function raises ``KeyError`` if a mandatory key is absent.
        If a validation function is provided, then a ``ValueError`` can be
        raised as well in some situations.
        """
        with self.lock:

            if default is not None:
                value = self.values.get(key, None)
                if value is None:
                    self.values[key] = default
                    value = default

            elif (is_mandatory or validate):
                try:
                    value = self.values[key]
                except KeyError:
                    raise KeyError(u"Missing '{}' in context".format(key))

            else:
                try:
                    value = self.values[key]
                except KeyError:
                    value = None

            if validate and validate(value) is False:
                raise ValueError(
                    u"Invalid value for '{}' in context".format(key))

            if filter:

                if value == default:
                    default = None  # else kills filtering of empty variables

                self.values[key] = self.filter(value, default)

    @classmethod
    def _filter(self, value, default=None):
        """
        Loads a value from the environment

        :param value: if it starts with '$',
            then it names an environment variable
        :type value: str

        :param default: the default value if no variable can be found
        :type default: str

        :return: the same or a different text string
        :rtype: str

        If the string provided starts with the char '$', then the function
        looks for an environment variable of this name and returns its value::

            >>>print(context._filter('$HOME'))
            /Users/bernard

        This is useful if you want to secure your configuration files.
        Instead of putting secrets in these files, you can store them
        in the environment, and only make a reference.

        Example::

            context = Context({
                'spark': {
                    'token': '$MY_BOT_TOKEN',
                    'weird_token', '$WEIRD_TOKEN',
                }
            })

            context.check('spark.token', filter=True)
            context.check('spark.weird_token', filter=True)

        """

        if value is None or len(value) < 1 or value[0] != '$':
            return value

        imported = os.environ.get(value[1:], default)
        if imported is None:
            logging.warning(u"Missing {} in environment".format(value))
        return imported

    def has(self, prefix):
        """
        Checks the presence of some prefix

        :param prefix: key prefix to be checked
        :type prefix: str

        :return: True if one or more key start with the prefix, else False

        This function looks at keys actually used in this context,
        and return True if prefix is found. Else it returns False.

        Example::

            context = Context(settings={'space': {'title', 'a title'}})

            >>>context.has('space')
            True

            >>>context.has('space.title')
            True

            >>>context.has('spark')
            False

        """
        with self.lock:

            for key in self.values.keys():
                if key.startswith(prefix):
                    return True

        return False

    def get(self, key, default=None):
        """
        Retrieves the value of one configurationkey

        :param key: name of the value
        :type key: str

        :param default: default value
        :type default: any serializable type is accepted

        :return: the actual value, or the default value, or None

        Example::

            message = context.get('bot.on_start')

        This function is safe on multiprocessing and multithreading.

        """
        with self.lock:

            value = self.values.get(key)

            if value is not None:
                return value

            values = {}
            for label in self.values.keys():
                if label.startswith(key+'.'):
                    values[label[len(key)+1:]] = self.values[label]
            if values.keys():
                return values

            return default

    def set(self, key, value):
        """
        Changes the value of one configuration key

        :param key: name of the value
        :type key: str

        :param value: new value
        :type value: any serializable type is accepted

        Example::

            context.set('bot.on_start', 'hello world')

        This function is safe on multiprocessing and multithreading.

        """
        with self.lock:

            self.values[key] = value

    def increment(self, key, delta=1):
        """
        Increments a value
        """
        with self.lock:

            value = self.values.get(key, 0)
            if not isinstance(value, int):
                value = 0
            value += delta
            self.values[key] = value

            return value

    def decrement(self, key, delta=1):
        """
        Decrements a value
        """
        with self.lock:

            value = self.values.get(key, 0)
            if not isinstance(value, int):
                value = 0
            value -= delta
            self.values[key] = value

            return value

    @classmethod
    def set_logger(cls, level=logging.DEBUG):
        """
        Configure logging

        :param level: expected level of verbosity

        This utility function should probably be put elsewhere
        """
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(asctime)-2s %(log_color)s%(message)s",
            datefmt='%H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
        handler.setFormatter(formatter)

        logging.getLogger('').handlers = []
        logging.getLogger('').addHandler(handler)

        logging.getLogger('').setLevel(level=level)
