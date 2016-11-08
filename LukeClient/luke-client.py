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

import os

from ConfigParser import ConfigParser
from requests import post

from LukeClient.Cpu import Cpu
from LukeClient.Disks import Disks
from LukeClient.Nics import Nics
from LukeClient.PollingStatus import PollingStatus
from LukeClient.Ram import Ram
from LukeClient.Server import Server
from LukeClient.utils.Utils import convert_to_json, produce_command

# get Luke's server uri
configs = ConfigParser()
configs.read('/etc/luke-client.conf')
lukeUri = configs.get('default', 'SERVER-URI')

# make sure we have connectivity, etc.
for nic in produce_command("ifconfig -a | sed 's/[ \t].*//;/^\(lo:\|\s*$\)/d'").split():
    os.system("dhclient {}".format(nic))

# generate and send report
server = Server(cpu=Cpu(), ram=Ram(), nics=Nics(), disks=Disks())
serverObject = {'Vendor': server.vendor,
                'Model': server.model,
                'Cpu': server.serverCpu.cpuObject,
                'Ram': server.serverRam.ramObject,
                'NICs': server.serverNics.nicsObject,
                'Disks': server.serverDisks.disksObject}


report = convert_to_json(serverObject)


bare_metal_id = post("{}/baremetal/".format(lukeUri),
                     data={"bare_metal": report}).content
bare_metal_id = bare_metal_id[1:-1]

polling_thread = PollingStatus(lukeUri, bare_metal_id)
polling_thread.start()
