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
import os
import re

from .OSCommitter import OSCommitter


class CleanCommitter(OSCommitter):
    def __init__(self):
        OSCommitter.__init__(self)

    def commit(self, bare_metal, request):
        filestr = get_filename
        protocol = re.sub('^([a-z]*)://.*$', '\1', filestr)
        host = re.sub('^[a-z]*://([^/]*)/.*$', '\1', filestr)
        path = re.sub('^[a-z]*://[^/]*/(.*)$', '\1', filestr)
        if protocol == "ssh":
            os.system("ssh {} 'dd if={}' | dd of=/dev/sda".format(host, path))


def get_filename():
    return "ssh://host/path"