u"""
Copyright 2016-2017 Hermann Krumrey

This file is part of xdcc-dl.

xdcc-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-dl.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
from __future__ import absolute_import
import unittest
from xdcc_dl.xdcc.layers.xdcc.XDCCInitiator import XDCCInitiator


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dcc_check(self):

        class Tester(XDCCInitiator):

            def on_welcome(self, conn, event):
                event.arguments = [u"NOTDCC"]
                self.on_ctcp(conn, event)
                raise TestException()

        try:
            Tester(u"irc.namibsun.net", u"random").start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)

    # HelloKitty no longer exists
    # def test_missing_whois(self):
    #    BotChannelMapper.bot_channel_map = {}
    #
    #    try:
    #        initiator = XDCCInitiator("irc.rizon.net", "random")
    #        initiator.current_pack = \
    #            XDCCPack(IrcServer("irc.rizon.net"), "HelloKitty", 1)
    #        initiator.start()
    #        self.assertTrue(False)
    #    except NoValidWhoisQueryException:
    #        self.assertTrue(True)
