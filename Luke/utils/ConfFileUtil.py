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

from ConfigParser import NoOptionError
from ConfigParser import NoSectionError
from ConfigParser import SafeConfigParser

FAKE_SECTION = 'asection'


class ConfFileUtil(SafeConfigParser):

    def get_option(self, option, raw=False, vars=None):
        """override of get function to use it without passing specific section

        :param option:
        :param raw:
        :param vars:
        :return:
        """
        res = None
        try:
            res = self.get(FAKE_SECTION, option, raw, vars)
        except NoSectionError as nse:
            print("calc_score: " + "NoSectionError " + nse.message)
        except NoOptionError as noe:
            print("calc_score: " + "NoOptionError " + noe.message)
        return res

    @staticmethod
    def read_from_conf_file(conf_file):
        parser = ConfFileUtil()
        parser.readfp(FakeSectionHead(open(conf_file)))
        return parser


class FakeSectionHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[' + FAKE_SECTION + ']\n'

    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()
