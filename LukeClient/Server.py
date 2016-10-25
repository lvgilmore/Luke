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
from LukeClient.Cpu import Cpu
from LukeClient.Ram import Ram
from LukeClient.Disks import Disks
from LukeClient.Nics import Nics


class Server(object):
    def __init__(self, cpu=None, ram=None, nics=None, disks=None):
        self.vendor = self.init_vendor()
        self.model = self.init_model()

        self.serverCpu = cpu if cpu is not None else Cpu()
        self.serverRam = ram if ram is not None else Ram()
        self.serverDisks = disks if disks is not None else Disks()
        self.serverNics = nics if nics is not None else Nics()

    @staticmethod
    def init_vendor():
        # for my laptop, "sudo dmidecode | grep -w 'Manufacturer:' | head -1" returned better results..
        # anyway, I added the sed to cut the key and save only the value
        return produce_command("sudo dmidecode | grep -w 'Vendor:' | sed 's/^.*: //'")

    @staticmethod
    def init_model():
        return produce_command(
            "sudo dmidecode -t system | awk -F: '$1~/Product Name/' | sed 's/^.*: //'")
