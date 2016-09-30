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

from ipaddr import IPv4Network
from os import remove
import unittest

import Luke.utils.DHCPConfParser as DHCPConfParser
from Luke.utils.DHCPConfParser import ParseError

SAMPLE_FILE = "/tmp/dhcpd.conf"

class TestParser(unittest.TestCase):

    def setUp(self):
        with open(SAMPLE_FILE, 'w') as f:
            f.write("""
            option subnet-mask 255.255.255.0;
            default-lease-time 600;
            shared-networks shit {
                subnet 192.168.0.0 netmask 255.255.255.0{
                    host 192.168.0.3 {
                        hardware ethernet 00:11:22:33:44:55 ;
                    }
                    range 192.168.2.10, 192.168.2.100 ;
                }
                group hey {
                    host 192.168.1.3 {
                        hardware ethernet 00:11:22:33:44:66 ;
                    }
                }
            }
            """)

    def tearDown(self):
        remove(SAMPLE_FILE)

    def test_preformat(self):
        valid = """#this is line comment
        subnet 10.0.0.0 netmask 255.255.0.0 { #this is another comment
        \toption routers 10.0.0.1;
        }"""
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

    def test_parse_host(self):
        key, value = DHCPConfParser._parse_host(['host shit', '{', '}'])
        self.assertEqual(key, 'shit')
        self.assertEqual(value, {'options': {}})

        self.assertRaises(ParseError, DHCPConfParser._parse_host,
                          ['host', '{'])
        self.assertRaises(ParseError, DHCPConfParser._parse_host,
                          ['host shit', '{', ';'])

    def test_parse_subnet(self):
        key, value = DHCPConfParser._parse_subnet(
            ['subnet 192.168.0.0 netmask 255.255.0.0', '{', '}'])
        self.assertEqual(str(key), "192.168.0.0/16")
        self.assertEqual(value, {'hosts': {},
                                 'options': {},
                                 'groups': {}
                                 })

        self.assertRaises(ParseError, DHCPConfParser._parse_subnet,
                          ['subnet 192.168.0.0 netmask 255.255.0.0', ';'])

    def test_parse_shared_net(self):
        key, value = DHCPConfParser._parse_shared_network(
            ['shared-network shit', '{', '}'])
        self.assertEqual(key, 'shit')
        self.assertEqual(value, {'hosts': {},
                                 'options': {},
                                 'groups': {},
                                 'subnets': {},
                                 })

    def test_parse_group(self):
        key, value = DHCPConfParser._parse_group(
            ['group shit', '{', '}'])
        self.assertEqual(key, 'shit')
        self.assertEqual(value, {'hosts': {},
                                 'options': {},
                                 'shared-networks': {},
                                 'subnets': {},
                                 'groups': {},
                                 })

    def test_parse(self):
        configs = DHCPConfParser.load(SAMPLE_FILE)
        expected = {
            'globals': {
                'option subnet-mask': '255.255.255.0',
                'default-lease-time': '600',
            },
            'subnets': {},
            'hosts': {},
            'groups': {},
            'shared-networks': {
                'shit': {
                    'hosts': {},
                    'options': {},
                    'groups': {
                        'hey': {
                            'hosts': {
                                '192.168.1.3': {
                                    'options': {
                                        'hardware':
                                            ['ethernet', '00:11:22:33:44:66']
                                    }
                                }
                            },
                            'options': {},
                            'shared-networks': {},
                            'subnets': {},
                            'groups': {},
                        }
                    },
                    'subnets': {
                        IPv4Network("192.168.0.0/24"): {
                            'hosts': {
                                '192.168.0.3': {
                                    'options': {
                                        'hardware':
                                            ['ethernet', '00:11:22:33:44:55']
                                    }
                                }
                            },
                            'options': {
                                'range': ['192.168.2.10,', '192.168.2.100']
                            },
                            'groups': {},
                        }
                    },
                }
            }
        }
        self.assertEqual(configs, expected)


if __name__ == '__main__':
    unittest.main()
