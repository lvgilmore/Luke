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

from time import sleep
from requests import get
from unittest import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Luke.API.settings")


class TestDjangoViews(TestCase):

    @classmethod
    def setUpClass(cls):
        newpid = os.fork()
        if newpid == 0:
            manager = os.path.join(os.path.dirname(__file__), "../../Luke/manage.py")
            os.execv(manager, ["manage.py", "runserver"])
        else:
            sleep(1)

    @classmethod
    def tearDownClass(cls):
        killpid = int(os.popen("ps -f | awk '/manage.py/ {print $2}' | head -1").read())
        os.kill(killpid, 15)

    def test_add_req(self):
        response = get('http://localhost:8000/request')
        self.assertEqual(response.content, 'good get')
