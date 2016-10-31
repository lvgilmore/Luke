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
import json
import os
import threading

import time
from requests import post
from requests import get
from requests import put

from Luke.common.Status import Status
from LukeClient.Cpu import Cpu
from LukeClient.Disks import Disks
from LukeClient.Nics import Nics
from LukeClient.PollingStatus import PollingStatus
from LukeClient.Ram import Ram
from LukeClient.Server import Server

os.system("dhclient eth0")
server = Server(cpu=Cpu(), ram=Ram(), nics=Nics(), disks=Disks())
serverObject = {'Vendor': server.vendor,
                'Model': server.model,
                'Cpu': server.serverCpu.cpuObject,
                'Ram': server.serverRam.ramObject,
                'NICs': server.serverNics.nicsObject,
                'Disks': server.serverDisks.disksObject}
port = 8000

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

time.sleep(3)
polling_thread = PollingStatus(port, bare_metal_id)
polling_thread.start()

# # Poll every 3 seconds
# bm = polling.poll(
#     lambda: get('http://localhost:{}/baremetal/{}'.format(port, bare_metal_id)),
#     step=3,
#     poll_forever=True)
#
# baremetal_status = str(json.loads(bm.content)['status'])
#
# print "bare metal is: " + baremetal_status






