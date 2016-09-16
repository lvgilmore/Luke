#! /usr/bin/python2.7

"""
@author: Geiger
@created: 13/09/2016
"""
from ipaddr import IPv4Network
from re import split
from re import sub


def load(conffile):
    dhcp_confs = {"shared_nets": {},
                  "subnets": {},
                  "hosts": {},
                  "groups": {},
                  "globals": {},
                  }
    confs = _preformat(conffile)
    while confs.__len__() > 0:
        conf = confs[0]
        if not isinstance(conf, str):
            raise TypeError("conf {} is {}. expected string".format(
                conf, str(conf.__class__)))
        if conf.startswith('shared-network'):
            k, v = _parse_shared_network(confs)
            dhcp_confs["shared_nets"][k] = v
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
    raw_conf = split('(\n|\{|\}|;)', conffile.read())
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
    assert isinstance(confs[0], str) \
        and confs[0].startswith('shared-network') \
        and confs[1] == '{'
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
    assert isinstance(confs[0], str) \
        and confs[0].startswith('subnet') \
        and confs[1] == '{'
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
    host_name = confs.pop(0).split()[1]
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
        raise IndexError("ended unexpectedly. expected ;")

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
    """
    :type configurations: dict
    :type conf_file: file or str
    :return: None
    """
    confs = {
        "confstring": "",
        "indent": 0,
        "raw": None
    }
    while configurations:
        key, confs["raw"] = configurations.popitem()
        if key == "options" or key == "globals":
            confs = _build_options(confs)
        elif key == "subnets":
            confs = _build_subnets(confs)
        elif key == "shared_networks":
            confs = _build_shared_networks(confs)
        elif key == "hosts":
            confs = _build_hosts(confs)
        elif key == "groups":
            confs = _build_groups(confs)
        else:
            raise ParseError
    f = open(conf_file, 'w')
    f.write(confs["confstring"])
    f.close()


def _build_options(confs):
    while confs["raw"]:
        key, value = confs["raw"].popitem()
        confs["confstring"] += "\t" * confs["indent"]
        confs["confstring"] += str(key) + " " + str(value) + ";\n"
    return confs


def _build_subnets(confs):
    subnet_name, subnet =confs["raw"]
    confs["confstring"] += "\t" * confs["indent"]
    ip, mask = IPv4Network(subnet_name).with_netmask.split("/")
    confs["confstring"] += "subnet" + ip + "netmask" + mask + "{"
    confs["indent"] += 1
    while subnet:
        key, confs["raw"] = subnet.popitem()
        if key == "options" or key == "globals":
            confs = _build_options(confs)
        elif key == "hosts":
            confs = _build_hosts(confs)
        elif key == "groups":
            confs = _build_groups(confs)
        else:
            raise ParseError
    confs["indent"] -= 1
    confs["confstring"] += "\t" * confs["indent"] + "}"
    return confs


def _build_shared_networks(confs):
    sharednet_name, sharednet = confs["raw"]
    confs["confstring"] += "\t" * confs["indent"]
    confs["confstring"] += "shared-network" + sharednet_name + "{"
    confs["indent"] += 1
    while sharednet:
        key, confs["raw"] = sharednet.popitem()
        if key == "options" or key == "globals":
            confs = _build_options(confs)
        elif key == "hosts":
            confs = _build_hosts(confs)
        elif key == "groups":
            confs = _build_groups(confs)
        elif key == "subnets":
            confs = _build_subnets(confs)
        else:
            raise ParseError
    confs["indent"] -= 1
    confs["confstring"] += "\t" * confs["indent"] + "}"
    return confs


def _build_hosts(confs):
    hostname, host = confs["raw"]
    confs["confstring"] += "\t" * confs["indent"]
    confs["confstring"] += "host" + hostname + "{"
    confs["indent"] += 1
    while host:
        key, confs["raw"] = host.popitem()
        if key == "options" or key == "globals":
            if not 'option hostname' in confs['options']:
                confs['options']['option hostname'] = hostname
            confs = _build_options(confs)
        else:
            raise ParseError
    confs["indent"] -= 1
    confs["confstring"] += "\t" * confs["indent"] + "}"
    return confs

def _build_groups(confs):
    group_name, group = confs["raw"]
    confs["confstring"] += "\t" * confs["indent"]
    confs["confstring"] += "group" + group_name + "{"
    confs["indent"] += 1
    while group:
        key, confs["raw"] = group.popitem()
        if key == "options" or key == "globals":
            confs = _build_options(confs)
        elif key == "hosts":
            confs = _build_hosts(confs)
        elif key == "groups":
            confs = _build_groups(confs)
        elif key == "subnets":
            confs = _build_subnets(confs)
        elif key == "shared-networks":
            confs = _build_shared_networks(confs)
        else:
            raise ParseError
    confs["indent"] -= 1
    confs["confstring"] += "\t" * confs["indent"] + "}"
    return confs


class ParseError(Exception):
    pass
