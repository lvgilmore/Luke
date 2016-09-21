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

class BareMetal:
    def __init__(self, bare_metal_str):
        self.bare_metal = bare_metal_str
    #     self.handle_new_bare_metal(bare_metal_str)
    #
    # @staticmethod
    # def handle_new_bare_metal(bare_metal_str):
    #     json_bare_metal = JsonUtils.convert_from_json_to_obj(bare_metal_str)
    #
    #     request = MatchMaker().find_match(json_bare_metal)
    #     print request


if __name__ == "__main__":
    BareMetal("{\"name\": \"name1\", \"url\": \"url\"}")
