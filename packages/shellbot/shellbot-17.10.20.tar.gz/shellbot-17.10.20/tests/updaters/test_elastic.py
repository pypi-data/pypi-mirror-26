#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from elasticsearch import ConnectionError
import gc
import logging
import mock
from multiprocessing import Process, Queue
import os
import sys

from shellbot import Context, Engine
from shellbot.events import Message
from shellbot.updaters import ElasticsearchUpdater

my_engine = Engine()


class UpdaterTests(unittest.TestCase):

    def tearDown(self):
        collected = gc.collect()
        logging.info("Garbage collector: collected %d objects." % (collected))

    def test_init(self):

        logging.info('***** init')

        u = ElasticsearchUpdater()
        self.assertEqual(u.engine, None)

        u = ElasticsearchUpdater(engine=my_engine)
        self.assertEqual(u.engine, my_engine)

    def test_on_init(self):

        logging.info('***** on_init')

        u = ElasticsearchUpdater()
        self.assertEqual(u.host, None)

        u = ElasticsearchUpdater(host=None)
        self.assertEqual(u.host, None)

        u = ElasticsearchUpdater(host='')
        self.assertEqual(u.host, '')

        u = ElasticsearchUpdater(host='elastic.acme.com')
        self.assertEqual(u.host, 'elastic.acme.com')

    def test_get_host(self):

        logging.info('***** get_host')

        u = ElasticsearchUpdater(engine=my_engine)
        self.assertEqual(u.get_host(), 'localhost:9200')

        u = ElasticsearchUpdater(engine=my_engine, host=None)
        self.assertEqual(u.get_host(), 'localhost:9200')

        u = ElasticsearchUpdater(engine=my_engine, host='')
        self.assertEqual(u.get_host(), 'localhost:9200')

        u = ElasticsearchUpdater(engine=my_engine, host='elastic.acme.com')
        self.assertEqual(u.get_host(), 'elastic.acme.com')

    def test_on_bond(self):

        logging.info('***** on_bond')

        u = ElasticsearchUpdater(host='this.does.not.exist')
        with self.assertRaises(Exception):
            u.on_bond(bot='*dummy')

    def test_put(self):

        logging.info('***** put')

        class FakeDb(object):
            def __init__(self):
                self.expected = None
            def index(self, index, doc_type, body):
                assert index == 'shellbot'
                assert doc_type == 'event'
                assert body == self.expected

        u = ElasticsearchUpdater()
        u.db = FakeDb()

        message_1 = Message({
            'person_label': 'alice@acme.com',
            'text': 'a first message',
        })
        u.db.expected = message_1.attributes
        u.put(message_1)

        message_2 = Message({
            'person_label': 'bob@acme.com',
            'text': 'a second message',
        })
        u.db.expected = message_2.attributes
        u.put(message_2)


if __name__ == '__main__':

    Context.set_logger()
    sys.exit(unittest.main())
