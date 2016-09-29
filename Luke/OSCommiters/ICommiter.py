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
Interface for specific OS commiters
@author: Geiger
@created: 11/09/2016
"""


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


class MethodNotImplementedError(NotImplementedError):
    def __init__(self, *args):
        NotImplementedError(*args)
