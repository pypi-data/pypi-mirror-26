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

from shellbot import Command


class Explore(Command):
    keyword = u'explore'
    information_message = u'Explore a planet and come back'
    usage_message = u'explore <destination>'

    def execute(self, bot, arguments=None, **kwargs):
        """
        Explores a planet and comes back
        """

        if not arguments:
            bot.say(u"usage: {}".format(self.usage_message))
            return

        bot.rocket.go('explore', arguments)
