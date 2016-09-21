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

from os import remove
import unittest

import Luke.utils.DHCPConfParser as DHCPConfParser
from Luke.utils.DHCPConfParser import ParseError

SAMPLE_FILE = "/tmp/dhcpd.conf"
valid = """#this is line comment
subnet 10.0.0.0 netmask 255.255.0.0 { #this is another comment
\toption routers 10.0.0.1;
}"""
#        invalid = "#shity shit" \
#                  "subnet 10.0.0.0 netmask {" \
#                  "\t\t\t option routers 10.0.0.1"


class TestParser(unittest.TestCase):

    def setUp(self):



        with open(SAMPLE_FILE, 'w') as f:
            f.write(valid)
            f.close()

    def tearDown(self):
        remove(SAMPLE_FILE)

    def test_preformat(self):
        confs = DHCPConfParser._preformat(valid)
        self.assertEqual(confs, ['subnet 10.0.0.0 netmask 255.255.0.0',
                                 '{', 'option routers 10.0.0.1', ';', '}'])

    def test_parse_option(self):
        key, value = DHCPConfParser._parse_option(['option shit 1 2 3', ';'])
        self.assertEqual(key, "option shit")
        self.assertEqual(value, ["1", "2", "3"])

        key, value = DHCPConfParser._parse_option(['shit 1 2 3', ';'])
        self.assertEqual(key, "shit")
        self.assertEqual(value, ["1", "2", "3"])

        key, value = DHCPConfParser._parse_option(['shit 1', ';'])
        self.assertEqual(key, "shit")
        self.assertEqual(value, "1")

        self.assertRaises(ParseError, DHCPConfParser._parse_option,
                          ['shit 1'])

#    def test_


if __name__ == '__main__':
    unittest.main()
