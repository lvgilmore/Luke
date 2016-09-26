#! /usr/bin/python2.7

"""
Interface for specific OS commiters
@author: Geiger
@created: 11/09/2016
"""

from json import dumps


class ICommiter(object):
    def __init__(self):
        pass

    def commit(self, bare_metal, request):
        """commits decision

        :param kwargs: dict
         :param host: Host
         :param os: OS
        :return: null
        """
        raise MethodNotImplementedError("you must implement commit")

    @staticmethod
    def normalize(argument, desired_type):
        if isinstance(argument, desired_type):
            return argument
        elif isinstance(argument, str):
            return desired_type(argument)
        elif isinstance(argument, dict) or isinstance(argument, list):
            return desired_type(dumps(argument))


class MethodNotImplementedError(NotImplementedError):
    def __init__(self, *args):
        NotImplementedError(*args)
