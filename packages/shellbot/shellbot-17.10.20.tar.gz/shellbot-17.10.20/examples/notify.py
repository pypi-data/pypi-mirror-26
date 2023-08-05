#!/usr/bin/env python
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

"""
Notify

In this example we use the bot only for easy notifications to a space.
There is no command in the shell at all, and the bot is not even started.

Multiple questions are adressed in this example:

- How to create a bot and configure it in one line? The simplest approach is to
  set environment variables and then to create the bot. This can be done
  externally, before running the program, for secret variables such as the
  Cisco Spark token (see below). Or variables can be set directly from within
  the script itself, as ``CHAT_ROOM_TITLE`` in this example.

- How to create or to delete a channel? When you access a bot for the first
  time it is created automatically in the back-end platform. From a software
  perspective, call ``engine.get_bot()`` and this will give you a bot instance.

  The bot itself can be used when you have to delete a channel, with a call of
  ``bot.dispose()``.

- How to post a notification? Use ``bot.say()`` on the bot instance. Messages
  posted can feature bare or rich text, and you can also upload an image or
  a document file.

- Why do we not start the bot? There is no call to 
  ``bot.run()`` here because there is no need for an active shell.
  The program updates a channel, however is not interactive and cannot answer
  messages send to it. Of course, it is easy to implement a couple of commands
  at some point so that you evolve towards a responsive bot.


To run this script you have to provide a custom configuration, or set
environment variables instead::

- ``CHANNEL_DEFAULT_PARTICIPANTS`` - Mention at least your e-mail address
- ``CISCO_SPARK_BOT_TOKEN`` - Received from Cisco Spark on bot registration
- ``SERVER_URL`` - Public link used by Cisco Spark to reach your server

The token is specific to your run-time, please visit Cisco Spark for
Developers to get more details:

    https://developer.ciscospark.com/

For example, if you run this script under Linux or macOs with support from
ngrok for exposing services to the Internet::

    export CHANNEL_DEFAULT_PARTICIPANTS="alice@acme.com"
    export CISCO_SPARK_BOT_TOKEN="<token id from Cisco Spark for Developers>"
    export SERVER_URL="http://1a107f21.ngrok.io"
    python notify.py


credit: http://pythonfiddle.com/random-sentence-generator/
"""

import os
import random
import time

from shellbot import Engine, Context

def some_message():
    """Creates random sentence"""

    s_nouns = ["A dude", "My mom", "The king", "Some guy",
               "A cat with rabies", "A sloth", "Your homie",
               "This cool guy my gardener met yesterday", "Superman"]

    s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates",
               "hacks", "configures", "spies on", "retards", "meows on",
               "flees from", "tries to automate", "explodes"]

    p_nouns = ["These dudes", "Both of my moms", "All the kings of the world",
               "Some guys", "All of a cattery's cats",
               "The multitude of sloths living under your bed",
               "Your homies", "Like, these, like, all these people", "Supermen"]

    infinitives = ["to make a pie.", "for no apparent reason.",
                   "because the sky is green.", "for a disease.",
                   "to be able to make toast explode.",
                   "to know more about archeology."]

    return u"{} {} {} {}".format(random.choice(s_nouns),
                                 random.choice(s_verbs),
                                 random.choice(p_nouns).lower(),
                                 random.choice(infinitives))

if __name__ == '__main__':

    Context.set_logger()

    os.environ['CHAT_ROOM_TITLE'] = 'Notifications'
    engine = Engine(type='spark', configure=True)

    bot = engine.get_bot(reset=True)  # create a group channel

    for index in range(7):  # send notifications to the channel
        bot.say(some_message())
        time.sleep(5)

    bot.say(u"Nothing more to say")

    print("Press Ctl-C to stop this program")
    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass

    bot.dispose()  # delete the initial group channel
