#! /usr/bin/python2.7

"""
Basic workflow to commit the MatchMaker decision
@author: Geiger
@created: 11/09/2016
"""

from json import dumps
from logging import getLogger

from Luke.BareMetal import BareMetal
from Luke.DHCPCommiter import DHCPCommiter
from Luke.OSCommiters import COMMITERS
from Luke.Request import Request

logger = getLogger(__name__)


class CommitWorkflow(object):
    def __init__(self):
        self.dhcp_commiter = DHCPCommiter()

    def commit(self, bare_metal, request):
        bare_metal = CommitWorkflow.normalize(bare_metal, BareMetal)
        request = CommitWorkflow.normalize(request, Request)
        try:
            os_commiter = COMMITERS[request.os]["handler"]()
        except (AttributeError, KeyError):
            logger.warning("could not reliably determine the os commiter")
        self.dhcp_commiter.commit(bare_metal, request)
        return os_commiter.commit(bare_metal, request)

    @staticmethod
    def normalize(argument, desired_type):
        if isinstance(argument, desired_type):
            return argument
        elif isinstance(argument, str):
            return desired_type(argument)
        elif isinstance(argument, dict) or isinstance(argument, list):
            return desired_type(dumps(argument))
