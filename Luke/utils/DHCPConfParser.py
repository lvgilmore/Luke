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
"""
@author: Geiger
@created: 13/09/2016
"""
from re import split
from re import sub

from ipaddr import IPv4Network

from Luke.utils.Utils import open_read_close


def load(conffile):
    dhcp_confs = {"shared-networks": {},
                  "subnets": {},
                  "hosts": {},
                  "groups": {},
                  "globals": {},
                  }
    confs = open_read_close(conffile)
    confs = _preformat(confs)
    while confs.__len__() > 0:
        conf = confs[0]
        if not isinstance(conf, str):
            raise TypeError("conf {} is {}. expected string".format(
                conf, str(conf.__class__)))
        if conf.startswith('shared-network'):
            k, v = _parse_shared_network(confs)
            dhcp_confs["shared-networks"][k] = v
        elif conf.startswith('subnet'):
            k, v = _parse_subnet(confs)
            dhcp_confs["subnets"][k] = v
        elif conf.startswith('host'):
            k, v = _parse_host(confs)
            dhcp_confs["hosts"][k] = v
        elif conf.startswith('group'):
            k, v = _parse_group(confs)
            dhcp_confs["groups"][k] = v
        elif conf.startswith('{') or conf.startswith('}'):
            raise ParseError(
                "unexpected word: {}".format(str(conf)))
        else:
            k, v = _parse_option(confs)
            dhcp_confs["globals"][k] = v
    return dhcp_confs


def _preformat(conffile):
    raw_conf = split('(\n|\{|\}|;)', conffile)
    for index, content in enumerate(raw_conf):
        raw_conf[index] = sub('#.*$', '', content)
        raw_conf[index] = sub('^\s+', '', raw_conf[index])
        raw_conf[index] = sub('\s+$', '', raw_conf[index])
    # clean empty entries
    try:
        while True:
            raw_conf.pop(raw_conf.index(''))
    except ValueError:
        pass
    return raw_conf


def _parse_shared_network(confs):
    try:
        if not confs[0].startswith('shared-network') \
                or not confs[1] == '{':
            raise ParseError
    except (TypeError, IndexError):
        raise ParseError
    shared_name = confs.pop(0).split()[1]
    shared_net = {'subnets': {},
                  'hosts': {},
                  'groups': {},
                  'options': {},
                  }
    confs.pop(0)
    while confs[0] != '}':
        if confs[0].startswith('subnet'):
            k, v = _parse_subnet(confs)
            shared_net['subnets'][k] = v
        elif confs[0].startswith('host'):
            k, v = _parse_host(confs)
            shared_net['hosts'][k] = v
        elif confs[0].startswith('group'):
            k, v = _parse_group(confs)
            shared_net['groups'][k] = v
        else:
            k, v = _parse_option(confs)
            shared_net['options'][k] = v
    confs.pop(0)
    return shared_name, shared_net


def _parse_subnet(confs):
    try:
        if not confs[0].startswith('subnet') \
                or not confs[1] == '{':
            raise ParseError
    except (TypeError, IndexError):
        raise ParseError
    subnet_ip = IPv4Network("{}/{}".format(
        confs[0].split()[1], confs[0].split()[3]))
    subnet = {'hosts': {},
              'groups': {},
              'options': {},
              }
    confs.pop(0)
    confs.pop(0)
    while confs[0] != '}':
        if confs[0].startswith('host'):
            k, v = _parse_host(confs)
            subnet['hosts'][k] = v
        elif confs[0].startswith('group'):
            k, v = _parse_group(confs)
            subnet['groups'][k] = v
        else:
            k, v = _parse_option(confs)
            subnet['options'][k] = v
    confs.pop(0)
    return subnet_ip, subnet


def _parse_host(confs):
    assert isinstance(confs[0], str) \
        and confs[0].startswith('host') \
        and confs[1] == '{'
    try:
        host_name = confs.pop(0).split()[1]
    except IndexError:
        raise ParseError("host must have a name")
    host = {'options': {}}
    confs.pop(0)
    while confs[0] != '}':
        k, v = _parse_option(confs)
        host['options'][k] = v
    confs.pop(0)
    return host_name, host


def _parse_option(confs):
    try:
        if confs[1] != ';':
            raise ParseError(
                "expected separator ; after conf {}".format(confs[0]))
    except IndexError:
        raise ParseError("ended unexpectedly. expected ;")

    raw_option = confs.pop(0).split()
    if raw_option[0] in ["option"]:
        option_name = "{} {}".format(raw_option.pop(0), raw_option.pop(0))
    else:
        option_name = raw_option.pop(0)
    if raw_option.__len__() == 1:
        option = raw_option.pop(0)
    else:
        option = raw_option
    confs.pop(0)
    return option_name, option


def _parse_group(confs):
    assert isinstance(confs[0], str) \
        and confs[0].startswith('group') \
        and confs[1] == '{'
    group_name = confs.pop(0).split()[1]
    group = {'subnets': {},
             'hosts': {},
             'shared-networks': {},
             'options': {},
             'groups': {},
             }
    confs.pop(0)
    while confs[0] != '}':
        if confs[0].startswith('subnet'):
            k, v = _parse_subnet(confs)
            group['subnets'][k] = v
        elif confs[0].startswith('host'):
            k, v = _parse_host(confs)
            group['hosts'][k] = v
        elif confs[0].startswith('shared-network'):
            k, v = _parse_shared_network(confs)
            group['shared-networks'][k] = v
        elif confs[0].startswith('group'):
            k, v = _parse_group(confs)
            group['groups'][k] = v
        else:
            k, v = _parse_option(confs)
            group['options'][k] = v
    confs.pop(0)
    return group_name, group


def save(configurations, conf_file):
    """translate dict to dhcp.conf string and saves

    :type configurations: dict
    :type conf_file: file or str
    :return: None
    """
    confstring = ""
    indent = 0
    raw = None
    if not isinstance(configurations, dict):
        configurations = configurations.__dict__
    while configurations:
        if "options" in configurations:
            raw = configurations.pop("options")
            key = "options"
        elif "globals" in configurations:
            raw = configurations.pop("globals")
            key = "options"
        else:
            key, raw = configurations.popitem()

        if key == "options":
            confstring, indent = _build_options(confstring, indent, raw)
        elif key == "subnets":
            confstring, indent = _build_subnets(confstring, indent, raw)
        elif key == "shared_networks" or key == "shared_nets":
            confstring, indent = _build_shared_networks(
                confstring, indent, raw)
        elif key == "hosts":
            confstring, indent = _build_hosts(confstring, indent, raw)
        elif key == "groups":
            confstring, indent = _build_groups(confstring, indent, raw)
        else:
            raise ParseError
    f = open(conf_file, 'w')
    f.write(confstring)
    f.close()


def _build_options(confstring, indent, raw):
    for key, value in raw.iteritems():
        confstring += "\t" * indent
        confstring += str(key) + " " + _value_str(value=value) + ";\n"
    return confstring, indent


def _value_str(value):
    string = ""
    if isinstance(value, str):
        string += value
    elif isinstance(value, list):
        while value:
            string += _value_str(value.pop(0)) + " "
    else:
        string += str(value)
    return string


def _build_subnets(confstring, indent, raw):
    for subnet_name, subnet in raw.iteritems():
        confstring += "\t" * indent
        ip, mask = IPv4Network(subnet_name).with_netmask.split("/")
        confstring += "subnet " + ip + " netmask " + mask + "{\n"
        indent += 1
        for key, value in subnet.iteritems():
            if key == "options" or key == "globals":
                confstring, indent = _build_options(confstring, indent, value)
            elif key == "hosts":
                confstring, indent = _build_hosts(confstring, indent, value)
            elif key == "groups":
                confstring, indent = _build_groups(confstring, indent, value)
            else:
                raise ParseError
        indent -= 1
        confstring += "\t" * indent + "}\n"
    return confstring, indent


def _build_shared_networks(confstring, indent, raw):
    for sharednet_name, sharednet in raw.iteritems():
        confstring += "\t" * indent
        confstring += "shared-network " + sharednet_name + " {\n"
        indent += 1
        for key, value in sharednet.popitem():
            if key == "options" or key == "globals":
                confstring, indent = _build_options(confstring, indent, value)
            elif key == "hosts":
                confstring, indent = _build_hosts(confstring, indent, value)
            elif key == "groups":
                confstring, indent = _build_groups(confstring, indent, value)
            elif key == "subnets":
                confstring, indent = _build_subnets(confstring, indent, value)
            else:
                raise ParseError
        indent -= 1
        confstring += "\t" * indent + "}\n"
    return confstring, indent


def _build_hosts(confstring, indent, raw):
    for hostname, host in raw.iteritems():
        confstring += "\t" * indent
        confstring += "host " + hostname + " {\n"
        indent += 1
        for key, value in host.iteritems():
            if key == "options" or key == "globals":
                if 'option hostname' not in value:
                    value['option hostname'] = hostname
                    confstring, indent = _build_options(confstring,
                                                        indent, value)
            else:
                raise ParseError
        indent -= 1
        confstring += "\t" * indent + "}\n"
    return confstring, indent


def _build_groups(confstring, indent, raw):
    for group_name, group in raw.iteritems():
        confstring += "\t" * indent
        confstring += "group " + group_name + " {\n"
        indent += 1
        for key, value in group.iteritems():
            if key == "options" or key == "globals":
                confstring, indent = _build_options(confstring, indent, value)
            elif key == "hosts":
                confstring, indent = _build_hosts(confstring, indent, value)
            elif key == "groups":
                confstring, indent = _build_groups(confstring, indent, value)
            elif key == "subnets":
                confstring, indent = _build_subnets(confstring, indent, value)
            elif key == "shared-networks":
                confstring, indent = _build_shared_networks(confstring,
                                                            indent, value)
            else:
                raise ParseError
        indent -= 1
        confstring += "\t" * indent + "}\n"
    return confstring, indent


class ParseError(Exception):
    pass
