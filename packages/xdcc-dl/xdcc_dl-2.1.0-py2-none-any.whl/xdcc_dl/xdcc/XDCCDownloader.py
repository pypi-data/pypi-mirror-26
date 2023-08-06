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

from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.xdcc.layers.irc.BaseIrcClient import NetworkError
from xdcc_dl.xdcc.layers.irc.BotFinder import BotNotFoundException
from xdcc_dl.xdcc.layers.xdcc.DownloadHandler import DownloadHandler,\
    AlreadyDownloaded
from xdcc_dl.xdcc.layers.xdcc.XDCCInitiator import IncorrectFileSentException,\
    NoValidWhoisQueryException


class XDCCDownloader(DownloadHandler):
    u"""
    The XDCC Downloader that combines the capabilities of
    all XDCC Layers to offer a stable interface to download XDCC Packs
    """

    def download(self, packs, progress = None):
        u"""
        Downloads all XDCC packs specified. Optionally shares state with other
        threads using a Progress object.
        All packs need to connect to the same server

        :param packs:    The packs to download
        :param progress: Optional Progress object
        :return: Dictionary of packs mapped to status codes:
                   "OK":              Download was successful
                   "BOTNOTFOUND":     Bot was not found
                   "CHANNELJOINFAIL": Channel join failed, most likely due to
                                      missing whois information
                   "NETWORKERROR":    Download failed due to network error
                   "INCORRECT":       Sent file was not the correct file
                   "EXISTED":         File already existed and was
                                      completely downloaded
                   "OTHERSERVER":     If a pack was found that is hosted on a
                                      different server
        """
        self.progress = progress if progress is not None else\
            Progress(len(packs))
        self.pack_queue = packs
        self.pack_states = {}

        while len(self.pack_queue) > 0:

            self.current_pack = self.pack_queue.pop(0)

            if self.current_pack.get_server().get_address() != \
                    self.server.get_address():
                self.pack_states[self.current_pack] = u"OTHERSERVER"
                continue

            status_code = u"OK"

            try:
                self.start()
            except BotNotFoundException:
                status_code = u"BOTNOTFOUND"
            except NoValidWhoisQueryException:
                status_code = u"CHANNELJOINFAIL"
            except AlreadyDownloaded:
                status_code = u"EXISTED"
            except IncorrectFileSentException:
                status_code = u"INCORRECT"
            except NetworkError:
                status_code = u"NETWORKERROR"

            self.pack_states[self.current_pack] = status_code
            self.reset_connection_state()
            self.progress.next_file()

        self.quit()

        return self.pack_states
