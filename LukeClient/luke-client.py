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
from logging import getLogger

import polling as polling
from requests import post
from time import sleep
from requests import get
from requests import put

from Luke.MongoClient.MList import MList
from Luke.MongoClient.MRequestList import MRequestList
from Luke.Request import Request
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

# report = convert_to_json(serverObject)
report = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                     \"Type\": \"Twisted Pair\", \"ip\": \"192.168.0.4\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"ip\": \"192.168.0.5\", \"Model\": \"mod\"}"
port = 8000


req = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
              "\"Vendor\": \"vend\"}," \
              "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
              "\"NICs\": {\"ens33\": " \
              "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
              \"Type\": \"Twisted Pair\"}}," \
              " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
              "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
              "\"Model\": \"mod\", \"profile\": \"common\"}}"


request = post("http://localhost:{}/request/".format(port), data={"request": req})

print(str(report))

# bare_metal_id = post("http://localhost:{}/baremetal/".format(port),
#                      data={"bare_metal": str(report)})
bare_metal_id = post("http://localhost:{}/baremetal/".format(port),
                     data={"bare_metal": report}).content
print(bare_metal_id)

status = None

# Poll every 10 seconds
baremetal = polling.poll(
    lambda: get('http://localhost:{}/baremetal/{}'.format(port, bare_metal_id)).content,
    step=10,
    poll_forever=True)
print baremetal

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
