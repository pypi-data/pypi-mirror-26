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

import logging
from multiprocessing import Queue
import os

from shellbot.context import Context
from shellbot.i18n import _
from shellbot.speaker import Speaker, Vibes
from .base import Updater
from shellbot.spaces import SparkSpace


class SpaceUpdater(Updater):
    """
    Replicates messages to a secondary space
    """

    def on_init(self, space=None, speaker=None, **kwargs):
        """
        Replicates messages to a secondary space

        :param space: the target space to use (optional)
        :type space: Space

        :param speaker: the speaker instance to use (optional)
        :type speaker: Speaker

        Parameters are provided mainly for test injection.
        """

        # create a secondary room
        #
        self.space = space if space else SparkSpace(context=self.engine.context)

        self.space.connect()

        title = u"{} - {}".format(
            self.space.configured_title(), _(u"Audited content"))

        self.space.bond(title=title)

        # speak incoming updates
        #
        self.context = Context()
        self.mouth = Queue()

        self.speaker = speaker if speaker else Speaker(engine=self.engine)
        self.speaker.start()

    def put(self, event):
        """
        Processes one event

        :param event: an inbound event
        :type event: Event or Message or Join or Leave

        With this class a string representation of the received event
        is forwarded to the speaker queue of a chat space.
        """
        logging.debug(u"- updating with a {} event".format(event.type))
        logging.debug(event.attributes)

        if event.get('url'):
            attachment = self.space.download_attachment(event.url)
            message = _(u"{}: {}").format(event.from_label,
                                          os.path.basename(attachment))

            self.mouth.put(Vibes(text=message,
                                 file=attachment))

        else:
            self.mouth.put(self.format(event))

    def format(self, event):
        """
        Prepares an outbound line

        :param event: an inbound event
        :type event: Event or Message or Join or Leave

        :return: outbound line
        :rtype: str

        This function adapts inbound events to the appropriate
        format. It turns an object with multiple attributes
        to a single string that can be pushed to a Cisco Spark room.

        """
        if event.type == 'message':

            text = _(u"{}: {}")

            if event.content == event.text:
                return text.format(event.from_label, event.text)

            return Vibes(text=text.format(event.from_label, event.text),
                         content=text.format(event.from_label, event.content),
                         file=None)

        if event.type == 'join':
            return _(u"{} has joined").format(event.actor_label)

        if event.type == 'leave':
            return _(u"{} has left").format(event.actor_label)

        return _(u"an unknown event has been received")
