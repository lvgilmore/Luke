#! /usr/bin/python
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

import json
import os


def convert_to_json(object_to_convert):
    try:
        jsonification = json.dumps(object_to_convert)
    except TypeError:
        jsonification = json.dumps(object_to_convert.__dict__)
    # and now we can avoid sending "diskObject", etc.
    # however, sending instances here means we must be careful with properties
    return jsonification


def produce_command(command):
    f = os.popen(command)
    return f.read().strip()