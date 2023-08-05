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

from shellbot.i18n import _
from .base import Command


class Update(Command):
    """
    Update input data
    """

    keyword = _(u'update')
    information_message = _(u'Update input content')

    no_arg = _(u'Thanks to provide the key and the data')
    no_input = _(u'There is nothing to update, input is empty')
    ok_msg = _(u'Update successfuly done')

    def execute(self, bot, arguments=None, **kwargs):
        """
        Update input data

        :param bot: The bot for this execution
        :type bot: Shellbot

        :param arguments: The arguments for this command
        :type arguments: str or ``None``

        """
        if not arguments:
            bot.say(self.no_arg, content=self.no_arg)
            return

        input = bot.recall('input')
        if not input:
            bot.say(self.no_input)
            return

        tokens = arguments.split(' ')
        if len(tokens) < 2:
            bot.say(self.no_arg)
            return

        bot.update('input', tokens[0], tokens[1])
        bot.say(self.ok_msg)
