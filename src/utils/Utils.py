#! /usr/bin/python2.7

from ipaddr import IPv4Address, IPv4Network
import json


class Utils(object):

    @staticmethod
    def ip_to_subnet(ip="0.0.0.0"):
        ip = IPv4Network(ip)  # now it doesn't matter if we got ip as address, network or string
        if ip.prefixlen == 32:
            ip = IPv4Network(ip.__str__() + "/24")
        return ip

    @staticmethod
    def convert_from_json_to_obj(obj_to_convert):
        return json.loads(obj_to_convert)

    @staticmethod
    def write_json_to_file(json_obj):
        with open('Requests.json', 'a') as f:
            f.write("\n".format(json.dump(json_obj, f)))

        # with open('Requests.json', 'r') as f:
        #     data = json.load(f)
        #
        # dict.update(json_obj)
        #
        # with open('Requests.json', 'w') as f:
        #     json.dump(data, f)

    @staticmethod
    def read_json_from_file():
        with open('Requests.json', 'r') as f:
            data = json.load(f)

            # access content of data
            print data[0]["count"]
            # print data
