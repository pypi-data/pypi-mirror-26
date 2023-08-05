#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import gc
import json
import logging
from multiprocessing import Queue
import os
import sys
import yaml

from shellbot import Context
from shellbot.events import Event, Message, Join, Leave, EventFactory


class EventsTests(unittest.TestCase):

    def test_event_init(self):

        event = Event()
        self.assertEqual(event.type, 'event')
        self.assertEqual(event.attributes, {})

        event = Event(None)
        self.assertEqual(event.attributes, {})

        event = Event('')
        self.assertEqual(event.attributes, {})

        event = Event(attributes=None)
        self.assertEqual(event.attributes, {})

        event = Event(attributes='')
        self.assertEqual(event.attributes, {})

        data = {u'hellô': 'b', u'wörld': 123}
        event = Event(attributes=json.dumps(data))
        self.assertEqual(event.attributes, data)

        data = {u'hellô': 'b', u'wörld': 123}
        event = Event(attributes=data)
        self.assertEqual(event.attributes, data)

    def test_event___getattr__(self):

        event = Event()
        with self.assertRaises(AttributeError):
            value = event.unknown

        data = {u'hello': u'wörld', 'number': 123, 'weird': None}

        event = Event(attributes=data)
        self.assertEqual(event.hello, u'wörld')
        self.assertEqual(event.number, 123)
        self.assertEqual(event.weird, None)

        event = Event(attributes=json.dumps(data))
        self.assertEqual(event.hello, u'wörld')
        self.assertEqual(event.number, 123)
        self.assertEqual(event.weird, None)

    def test_event_get(self):

        event = Event()
        with self.assertRaises(AttributeError):
            value = event.unknown
        self.assertEqual(event.get('unknown'), None)
        self.assertEqual(event.get('unknown', 'hye'), 'hye')

        data = {u'hellô': u'wörld', 'number': 123, 'weird': None}

        event = Event(attributes=data)
        self.assertEqual(event.get(u'hellô'), u'wörld')
        self.assertEqual(event.get('number'), 123)
        self.assertEqual(event.get('weird'), None)
        self.assertEqual(event.get('weird', []), [])

        event = Event(attributes=json.dumps(data))
        self.assertEqual(event.get(u'hellô'), u'wörld')
        self.assertEqual(event.get('number'), 123)
        self.assertEqual(event.get('weird'), None)
        self.assertEqual(event.get('weird', []), [])

    def test_event___setattr__(self):

        data = {'personEmail': 'foo@acme.com'}
        event = Event(attributes=data)

        with self.assertRaises(AttributeError):
            value = event.person_name

        event.person_name = event.personEmail
        self.assertEqual(event.person_name, 'foo@acme.com')

    def test_event___repr__(self):

        event = Event()
        self.assertEqual(repr(event), 'Event({})')

    def test_event___str__(self):

        event = Event()
        self.assertEqual(str(event), '{"type": "event"}')

        data = {u'hellô': u'wörld', 'number': 123}
        event = Event(attributes=json.dumps(data))
        data.update({'type': 'event'})
        self.assertEqual(json.loads(str(event)), data)
        self.assertEqual(yaml.safe_load(str(event)), data)

    def test_event___eq__(self):

        a = Event({"hello": "world"})
        b = Event({"hello": "world"})
        self.assertEqual(a, b)

        a = Event({"hello": "world"})
        b = Event({"hello": "world"})
        self.assertTrue(a.__eq__(b))
        self.assertTrue(b.__eq__(a))

        a = Event({"hello": "world"})
        b = Event({"hello": "moon"})
        self.assertFalse(a.__eq__(b))
        self.assertFalse(b.__eq__(a))

        a = Event({"hello": "world"})
        b = Message({"hello": "world"})
        self.assertFalse(a.__eq__(b))
        self.assertFalse(b.__eq__(a))

        a = Event({"hello": "world"})
        b = {"hello": "world"}
        self.assertFalse(a.__eq__(b))

    def test_event_queue(self):

        data = {u'hello': u'wörld', 'number': 123, 'weird': None}
        before = Event(attributes=data)
        my_queue = Queue()
        my_queue.put(str(before))
        after = Event(my_queue.get())
        self.assertEqual(after.attributes, data)

    def test_message_init(self):

        event = Message()
        self.assertEqual(event.type, 'message')
        with self.assertRaises(AttributeError):
            message = event.text
        self.assertEqual(event.attachment, None)
        self.assertEqual(event.url, None)
        self.assertEqual(event.from_id, None)
        self.assertEqual(event.from_label, None)
        self.assertEqual(event.is_direct, False)
        self.assertEqual(event.mentioned_ids, [])
        self.assertEqual(event.channel_id, None)
        self.assertEqual(event.stamp, None)

    def test_message(self):

        item = {
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "content" : "<p>/plumby use containers/docker</p>",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = Message(item)
        self.assertEqual(event.type, 'message')
        self.assertEqual(event.channel_id,
                         "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0")
        self.assertEqual(event.text,
                         "/plumby use containers/docker")
        self.assertEqual(event.content,
                         "<p>/plumby use containers/docker</p>")
        self.assertEqual(event.stamp,
                         "2015-10-18T14:26:16+00:00")
        self.assertEqual(event.from_id,
                         "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY")
        self.assertEqual(event.from_label,
                         "Masked Cucumber")
        self.assertEqual(event.is_direct, True)
        self.assertEqual(event.mentioned_ids,
                         ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"])
        self.assertEqual(event.url, None)
        self.assertEqual(event.attachment, None)

        item.update({'type': 'message'})
        self.assertEqual(json.loads(str(event)), item)
        self.assertEqual(yaml.safe_load(str(event)), item)

        item = {
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = Message(item)
        self.assertEqual(event.text, event.content)

    def test_message_queue(self):

        item = {
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        before = Message(item)
        my_queue = Queue()
        my_queue.put(str(before))
        after = Message(my_queue.get())
        self.assertEqual(after.attributes, item)

    def test_join_init(self):

        event = Join()
        self.assertEqual(event.type, 'join')
        with self.assertRaises(AttributeError):
            value = event.actor_id
        with self.assertRaises(AttributeError):
            value = event.actor_label
        with self.assertRaises(AttributeError):
            value = event.channel_id

    def test_leave_init(self):

        event = Leave()
        self.assertEqual(event.type, 'leave')
        with self.assertRaises(AttributeError):
            value = event.actor_id
        with self.assertRaises(AttributeError):
            value = event.actor_label
        with self.assertRaises(AttributeError):
            value = event.channel_id

    def test_factory_message(self):

        item = {
              "type": "message",
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = EventFactory.build_event(item)
        self.assertTrue(isinstance(event, Message))
        self.assertEqual(event.type, 'message')

    def test_factory_join(self):

        item = {
              "type": "join",
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = EventFactory.build_event(item)
        self.assertTrue(isinstance(event, Join))
        self.assertEqual(event.type, 'join')

    def test_factory_leave(self):

        item = {
              "type": "leave",
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = EventFactory.build_event(item)
        self.assertTrue(isinstance(event, Leave))
        self.assertEqual(event.type, 'leave')

    def test_factory_void(self):

        item = {
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = EventFactory.build_event(item)
        self.assertTrue(isinstance(event, Event))
        self.assertEqual(event.type, 'event')

    def test_factory_unknown(self):

        item = {
              "type": "*really*unknown",
              "id" : "Z2lzY29zcGFyazovL3VzDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
              "channel_id" : "Y2lzY29zcGFyazovNmMS0zYLTkxNDctZjE0YmIwYzRkMTU0",
              "text" : "/plumby use containers/docker",
              "stamp" : "2015-10-18T14:26:16+00:00",
              "from_id" : "Y2lzY29zcGFyjOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
              "from_label" : "Masked Cucumber",
              "is_direct" : True,
              "mentioned_ids" : ["Y2lzYDMzLTRmYTUtYTcyYS1jYzg5YjI1ZWVlMmX"],
            }

        event = EventFactory.build_event(item)
        self.assertTrue(isinstance(event, Event))
        self.assertEqual(event.type, 'event')


if __name__ == '__main__':

    Context.set_logger()
    sys.exit(unittest.main())
