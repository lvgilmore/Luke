#! /usr/bin/python2.7

"""
Basic workflow to commit the MatchMaker decision
@author: Geiger
@created: 11/09/2016
"""

from logging import getLogger

from DHCPCommiter import DHCPCommiter
from OSCommiters import COMMITERS

logger = getLogger(__name__)


class CommitWorkflow(object):
    def __init__(self):
        self.dhcp_commiter = DHCPCommiter()

    def commit(self, bare_metal, request):
        if request["os"] in COMMITERS:
            os_commiter = COMMITERS[request["os"]]["handler"]()
        else:
            logger.warning("could not reliably determine the os commiter")

        self.dhcp_commiter.commit(bare_metal, request)
        os_commiter.commit(bare_metal, request)


# move to test file
"""
if __name__ == "__main__":
    cw = CommitWorkflow()
    assert isinstance(cw.dhcp_commiter, DHCPCommiter)
    cw.commit(host={"ip": "192.168.0.1/24"}, os="Rory")
    assert isinstance(cw.os_commiter, RoryCommiter)
"""
