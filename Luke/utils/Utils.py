#! /usr/bin/python2.7

from ipaddr import IPv4Network


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
