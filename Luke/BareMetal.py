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

from json import loads


class BareMetal(object):
    def __init__(self, bare_metal_str):
        self.bare_metal = bare_metal_str
        json_bare = loads(bare_metal_str)
        for key, value in json_bare.iteritems():
            self.__dict__[key] = value
        self.ip = json_bare['ip'] if 'ip' in json_bare else None
        if 'hostname' in json_bare:
            self.hostname = json_bare['hostname']
        elif self.ip:
            self.hostname = self.ip
        else:
            self.hostname = None


if __name__ == "__main__":
    BareMetal("{\"name\": \"name1\", \"url\": \"url\"}")
