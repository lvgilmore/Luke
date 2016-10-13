#! /usr/bin/python2.7
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
from json import loads
from unittest import TestCase
from unittest import main

from Luke.BareMetal import BareMetal
from Luke.OSCommiters.RoryCommiter import RoryCommiter
from Luke.Request import Request


class TestRoryCommiter(TestCase):

    def setUp(self):
        if 'LUKE_PATH' not in os.environ:
            os.environ['LUKE_PATH'] = os.path.join(os.path.dirname(__file__), "../../")
        self.roryc = RoryCommiter()

    def tearDown(self):
        pass

    def test_commit(self):
        req = """{"requirements": {"Cpu": {"Sockets": "1", "Arch": "x86_64",
            "Speed": "2201.000", "Cores": "1"},
             "Vendor": "vend"},
            "other_prop": {"profile": "shit"},
            "os": "Rory"} """
        json_req = json.loads(req)

        bare_metal = BareMetal(
            """{"Vendor": "vend", "Cpu": {"Sockets": "1", "Arch": "x86_64",
             "Speed": "2201.000", "Cores": "1"},
             "Ram": {"Size": "3062784"},
             "NICs": {"ens33": {"Speed": "Speed: 1000Mb/s",
             "Mac": "00:0c:29:3d:5e:ce", "Type": "Port: Twisted Pair"}},
             "Disks": {"sda": {"Vendor": "VMware", "Size": "2"},
             "sr0": {"Vendor": "VMware", "Size": "5"}},
             "Model": "mod", "ip": "192.168.0.1"}""")

        url, data = self.roryc.commit(bare_metal, Request(json_req))
        data = loads(data)
        self.assertEqual(url, "http://google.com/")
        self.assertEqual(data, {"profile": "shit",
                                "mac": "00:0c:29:3d:5e:ce",
                                "ip": "192.168.0.1"})


if __name__ == '__main__':
    main()
