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


class Empty(Command):
    """
    Handles empty command
    """

    keyword = _(u'*empty')
    information_message = _(u'Handle empty command')
    is_hidden = True

    def execute(self, bot, arguments=None, **kwargs):
        """
        Handles empty command

        :param bot: The bot for this execution
        :type bot: Shellbot

        :param arguments: The arguments for this command
        :type arguments: str or ``None``

        """
        if not hasattr(self, 'help_command'):
            self.help_command = self.engine.shell.command('help')

        if self.help_command is None:
            bot.say(_(u"No help command has been found."))

        else:
            self.help_command.execute(bot)
