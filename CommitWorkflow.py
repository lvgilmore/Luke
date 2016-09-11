#! /usr/bin/python2.7

"""
Basic workflow to commit the MatchMaker decision
@author: Geiger
@created: 11/09/2016
"""

from logging import getLogger, WARNING
from DHCPCommiter import DHCPCommiter
from OSCommiters import *



class CommitWorkflow():
    def __init__(self):
        self.dhcp_commiter = DHCPCommiter()
        self.os_commiter = None
        self.logger = getLogger(__name__)

    def commit(self, **kwargs):
        try:
            host = kwargs["host"]
            os = kwargs["os"]
        except KeyError:
            raise KeyError("CommitWorkflow.commit expects host and os kwargs")
        if COMMITERS.has_key(os):
            self.os_commiter = COMMITERS[os]["handler"]()
        else:
            self.logger.log(WARNING, "could not reliably determine the os commiter")

        self.dhcp_commiter.commit(**kwargs)
        self.os_commiter.commit(**kwargs)


if __name__ == "__main__":
    cw = CommitWorkflow()
    assert isinstance(cw.dhcp_commiter, DHCPCommiter)
    cw.commit(host={"ip": "192.168.0.1/24"}, os="Rory")
    assert isinstance(cw.os_commiter, RoryCommiter)
