#! /usr/bin/python2.7

"""
Interface for specific OS commiters
@author: Geiger
@created: 11/09/2016
"""


class ICommiter:
    def __init__(self):
        pass

    def commit(self, **kwargs):
        """

        :param kwargs: dict
         :param host: Host
         :param os: OS
        :return: null
        """
        raise MethodNotImplementedError("you must implement commit")


class MethodNotImplementedError(NotImplementedError):
    def __init__(self, *args):
        NotImplementedError(*args)