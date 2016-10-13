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
Basic workflow to commit the MatchMaker decision
@author: Geiger
@created: 11/09/2016
"""
import os

from json import dumps
from logging import getLogger

from .BareMetal import BareMetal
from .OSCommitters.committers import COMMITTERS
from .OSCommitters.DHCPCommitter import DHCPCommitter
from .Request import Request

logger = getLogger(__name__)


def commit(bare_metal, request):
    bare_metal = normalize(bare_metal, BareMetal)
    request = normalize(request, Request)
    os_committer = None
    try:
        os_committer = COMMITTERS[request.os]["handler"]()
    except (AttributeError, KeyError):
        logger.warning("could not reliably determine the os commiter")

    if "section" in COMMITTERS[request.os]:
        section = COMMITTERS[request.os]["section"]
    else:
        section = request.os
    request.other_prop["section"] = section

    DHCPCommitter().commit(bare_metal, request)

    return os_committer.commit(bare_metal, request)


def normalize(argument, desired_type):
    if isinstance(argument, desired_type):
        return argument
    elif isinstance(argument, str):
        return desired_type(argument)
    elif isinstance(argument, dict) or isinstance(argument, list):
        return desired_type(dumps(argument))