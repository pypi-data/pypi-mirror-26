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


class IrcServer(object):
    u"""
    Class that models an IRC server
    """

    def __init__(self, server_address, server_port = 6667):
        u"""
        Initializes the Server's information

        :param server_address: the address of the IRC Server
        :param server_port:    the port of the server, which defaults to 6667
                               and can usually safely stay that way
        """
        self.address = server_address
        self.port = server_port

    def get_address(self):
        u"""
        :return: the server address
        """
        return self.address

    def get_port(self):
        u"""
        :return: the server port
        """
        return self.port
