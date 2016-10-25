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

from LukeClient.utils.Utils import produce_command


class Disks(object):

    def __init__(self):

        self.allDisks = produce_command("lsblk | grep ^[a-z]  | awk '{print $1}'")
        self.disksObject = {}
        self.get_all_disks()

    def get_all_disks(self):
        disksList = {}
        for disk in self.allDisks.split():
            disksList.update(
                {disk: Disk(produce_command("sudo fdisk -l | grep /dev/sda: |awk '{print $3$4}'"),
                            produce_command("cat /sys/block/sd?/device/vendor"))})
        self.init_disks_object(disksList)

    def init_disks_object(self, disksList):
        for k, v in disksList.items():
            self.disksObject.update({k: v.diskObject})


if __name__ == '__main__':
    disks = Disks()
    print str(disks.disksList)
    print str(disks.disksObject)


class Disk(object):

    def __init__(self, size, vendor):
        self.diskObject = {'Size' : size,
                           'Vendor' : vendor}