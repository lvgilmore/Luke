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
from ipaddr import IPv4Network
from logging import getLogger
from os import popen
from re import sub

DHCP_LOG_FILE = "/var/log/dhcpd.log"
logger = getLogger(__name__)


def ip_to_subnet(ip="0.0.0.0"):
    ip = IPv4Network(ip)  # works the same for address, network and string
    if ip.prefixlen == 32:
        ip = IPv4Network(sub('/[0-9]*$', '', ip.__str__()) + "/24")
    return ip


def open_read_close(filename):
    f = open(filename)
    temp = f.read()
    f.close()
    return temp


def locate_mac_in_log(search_macs):
    macs = []
    log = popen("tail -500 {} | grep DHCPDISCOVER".format(
        DHCP_LOG_FILE)).read().split('\n')
    for line in log:
        mac = sub(
            r'^.*DHCPDISCOVER.*from '
            r'(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}).*',
            r'\1',
            line)
        if mac in search_macs:
            macs.append(mac)
    if len(macs) == 0:
        logger.warning("couldn't find mac in dhcp log")
        return False
    else:
        return macs[-1]
