#! /usr/bin/python
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from LukeClient.utils.Utils import produce_command


class Nics(object):

    def __init__(self):

        self.allDevices = produce_command("ifconfig -a | sed 's/[ \t].*//;/^\(lo:\|\s*$\)/d'")
        self.nicsObject = {}
        self.get_all_nics_list()

    def get_all_nics_list(self):
        nicsList = {}
        for device in self.allDevices.split():
              nicsList.update({device: Nic(
                  produce_command("ethtool " + device + " | grep 'Port' | sed 's/^.*: //'"),
                  produce_command("ethtool " + device + " | grep 'Speed' | sed 's/^.*: //'"),
                  produce_command("ifconfig " + device + " | grep HWaddr | awk '{print $5}' | sed 's/^.*: //'"))})
        self.init_nics_object(nicsList)

    def init_nics_object(self, nicsList):
        for k, v in nicsList.items():
            self.nicsObject.update({k: v.nicObject})

class Nic:

    def __init__(self, type, speed, mac):
        self.nicObject = {'Type' : type,
                          'Speed' : speed,
                          'Mac' : mac}
