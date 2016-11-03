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
from ConfigParser import ConfigParser
from unittest import TestCase
from unittest import main

from Luke.BareMetal import BareMetal
from Luke.OSCommitters.DHCPCommitter import DHCPCommitter
from Luke.Request import Request
from Luke.utils import DHCPConfParser

SECTION = 'SECTION'
example = """option subnet-mask 255.255.255.0;
default-lease-time 600;
option domain-name-servers 192.168.1.1, 192.168.1.2;
option domain-search "example.com";
max-lease-time 7200;
subnet 192.168.2.0 netmask 255.255.255.0{
    range 192.168.2.10, 192.168.2.100 ;
    option routers 192.168.2.254;
}
subnet 192.168.1.0 netmask 255.255.255.0{
    range 192.168.2.10, 192.168.2.100 ;
    option routers 192.168.2.254;
}
subnet 192.168.0.0 netmask 255.255.255.0{
    range 192.168.2.10, 192.168.2.100 ;
    option routers 192.168.2.254;
}
"""


class TestDHCPCommiter(TestCase):
    def setUp(self):
        self.parser = ConfigParser()
        if 'LUKE_PATH' not in os.environ or os.environ['LUKE_PATH'] == "":
            os.environ['LUKE_PATH'] = os.path.join(os.path.dirname(__file__), "../../")
        self.dhcp_cong_file = os.path.join(os.environ['LUKE_PATH'], "tests/helpers/dhcp-example.conf")
        self.commiter = DHCPCommitter(self.dhcp_cong_file)
        with open(self.dhcp_cong_file, 'w') as f:
            f.write(example)
            f.close()

    def tearDown(self):
        pass

    def test_commit(self):
        req = """{"requirements": {"Cpu": {"Sockets": "1", "Arch": "x86_64",
            "Speed": "2201.000", "Cores": "1"},
             "Vendor": "vend"},
            "other_prop": {"profile": "shit", "section": "Rory"},
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

        self.commiter.commit(bare_metal=bare_metal, request=Request(json_req))

        self.assertEqual(DHCPConfParser.load(self.dhcp_cong_file),
                         DHCPConfParser.load(os.path.join(os.environ['LUKE_PATH'],
                                                          "tests/helpers/dhcp-expected.conf")))


if __name__ == '__main__':
    main()
