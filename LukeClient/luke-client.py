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

import polling as polling
from requests import post
from time import sleep
from requests import get
from requests import put

from Luke.common import Status
from LukeClient.Cpu import Cpu
from LukeClient.Disks import Disks
from LukeClient.Nics import Nics
from LukeClient.Ram import Ram
from LukeClient.Server import Server
from LukeClient.utils.Utils import convert_to_json

os.system("dhclient eth0")
server = Server(cpu=Cpu(), ram=Ram(), nics=Nics(), disks=Disks())
serverObject = {'Vendor': server.vendor,
                'Model': server.model,
                'Cpu': server.serverCpu.cpuObject,
                'Ram': server.serverRam.ramObject,
                'NICs': server.serverNics.nicsObject,
                'Disks': server.serverDisks.disksObject}

report = convert_to_json(serverObject)

# bare_metal_id = post("http://localhost:{}/bare_metal/", report)
bare_metal_id = None

port = 8080
status = None

# Poll every 10 seconds
baremetal = polling.poll(
    lambda: get('http://localhost:{}/bare_metal/{}'.format(port, bare_metal_id)),
    step=10,
    poll_forever=True)

if baremetal is not None and \
                status is not baremetal['status']:
    status = baremetal['status']

    # update status
    put('http://localhost:{}/bare_metal/{}/{}'.format(port, bare_metal_id, status))

    if status is Status.matched:
        print "status changed to matched"
    elif status is Status.reboot:
        print "status changed to reboot"
    elif status is Status.done:
        print "status changed to done"
