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
from typing import List, Dict

from xdcc_dl.logging import Logger
from xdcc_dl.entities.User import User
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.xdcc.XDCCDownloader import XDCCDownloader


class MultipleServerDownloader(object):
    u"""
    Class that can handle downloading from various server sources
    """

    def __init__(self, user, logger = 0):
        u"""
        Creates a new multiple server downloader, without specifying the server

        :param user:    The user with which to log in
        :param logger:  The logger to use
        """
        self.user = user
        self.logger = logger
        self.current_downloader = None
        self.quit_called = False

    def download(self, packs, progress = None):
        u"""
        Downloads all XDCC packs specified. Optionally shares state with other
        threads using a Progress object

        :param packs: The packs to download
        :param progress: Optional Progress object
        :return: Dictionary of packs mapped to status codes:
                   "OK":           Download was successful
                   "BOTNOTFOUND":  Bot was not found
                   "NETWORKERROR": Download failed due to network error
                   "INCOMPLETE":   Download was incomplete
                   "EXISTED":      File already existed and
                                   was completely downloaded
        """
        results = {}

        packservers = {}

        for pack in packs:
            try:
                packservers[pack.get_server().get_address()].append(pack)
            except KeyError:
                packservers[pack.get_server().get_address()] = [pack]

        for server in packservers:

            if not self.quit_called:
                self.current_downloader = \
                    XDCCDownloader(IrcServer(server), self.user, self.logger)
                server_results = \
                    self.current_downloader.download(
                        packservers[server], progress
                    )

                for result in server_results:
                    results[result] = server_results[result]

        return results

    def quit(self):
        u"""
        Quits the current downloader and stops all downloads to come

        :return: None
        """
        if self.current_downloader is not None:
            self.current_downloader.quit()
        self.quit_called = True
