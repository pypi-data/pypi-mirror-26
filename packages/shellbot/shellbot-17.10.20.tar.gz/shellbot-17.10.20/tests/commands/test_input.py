#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging
import mock
from multiprocessing import Process, Queue
import os
import sys

from shellbot import Context, Engine, Shell, Vibes
from shellbot.stores import MemoryStore
from shellbot.commands import Input

my_engine = Engine(mouth=Queue())
my_engine.shell = Shell(engine=my_engine)


class Bot(object):
    def __init__(self, engine):
        self.engine = engine
        self.data = {}

    def say(self, text, content=None, file=None):
        self.engine.mouth.put(Vibes(text, content, file))

    def update(self, label, key, value):
        self.data[key] = value

    def recall(self, label):
        return self.data


my_bot = Bot(engine=my_engine)


class InputTests(unittest.TestCase):

    def test_init(self):

        logging.info('***** init')

        c = Input(my_engine)

        self.assertEqual(c.keyword, u'input')
        self.assertEqual(
            c.information_message,
            u'Display all input')
        self.assertFalse(c.is_hidden)

    def test_execute(self):

        logging.info('***** execute')

        c = Input(my_engine)

        c.execute(my_bot)
        self.assertEqual(
            my_engine.mouth.get().text,
            u'There is nothing to display')
        with self.assertRaises(Exception):
            my_engine.mouth.get_nowait()

        my_bot.update('input', 'PO#', '1234A')
        my_bot.update('input', 'description', 'part does not fit')
        c.execute(my_bot)
        self.assertEqual(
            my_engine.mouth.get().text,
            u'Input:\nPO# - 1234A\ndescription - part does not fit')
        with self.assertRaises(Exception):
            my_engine.mouth.get_nowait()


if __name__ == '__main__':

    Context.set_logger()
    sys.exit(unittest.main())
