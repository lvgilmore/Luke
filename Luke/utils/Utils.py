#! /usr/bin/python2.7

from ipaddr import IPv4Network
from logging import getLogger
from os import popen
from re import sub

DHCP_LOG_FILE = "/var/log/dhcpd.log"
logger = getLogger(__name__)


class Utils(object):

    @staticmethod
    def ip_to_subnet(ip="0.0.0.0"):
        ip = IPv4Network(ip)  # works the same for address, network and string
        if ip.prefixlen == 32:
            ip = IPv4Network(ip.__str__() + "/24")
        return ip

    @staticmethod
    def open_read_close(filename):
        f = open(filename)
        temp = f.read()
        f.close()
        return temp

    @staticmethod
    def locate_mac_in_log(locate_macs):
        macs = []
        log = popen("tail -500 {} | grep DHCPDISCOVER".format(
            DHCP_LOG_FILE)).read().split('\n')
        for line in log:
            mac = sub(
                r'^.*DHCPDISCOVER.*from '
                r'(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}).*',
                r'\1',
                line)
            if mac in locate_macs:
                macs.append(mac)
        if len(macs) == 0:
            logger.warning("couldn't find mac in dhcp log")
            return False
        else:
            return macs[-1]
