#!/usr/bin/env bash

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

# install the program itself
INSTALLCMD="yum"
which dnf > /dev/null 2>&1 && INSTALLCMD="dnf"
sudo $INSTALLCMD install -y mongodb mongodb-server

cp mongod.conf /etc/

# enable and start the service
if which systemctl > /dev/null 2>&1 ; then
    systemctl enable mongod.service
    systemctl start mongod.service
elif which chkconfig > /dev/null 2>&1 ; then
    chkconfig --level 345 mongod on
    service mongod start
elif which update-rc.d > /dev/null 2>&1 ; then
    update-rc.d mongod start 20 3 4 5
    service mongod start
else
    service mongod start
fi

# populate the db
mongo << EOF
use luke ;
db.createUser(
    {
        user: "ace",
        pwd: "shit",
        roles: [ { role: "userAdmin", db: "ace" },
                 { role: "readWrite", db: "ace" } ]
    }
)
EOF
