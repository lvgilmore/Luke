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


class Cpu:

    def __init__(self):

        self.sockets = Cpu.init_socket()
        self.cores = Cpu.init_cores()
        self.speed = Cpu.init_speed()
        self.arch = Cpu.init_arch()

        self.cpuObject = {'Sockets': self.sockets,
                          'Cores': self.cores,
                          'Speed': self.speed,
                          'Arch': self.arch}

    @staticmethod
    def init_socket():
        return produce_command("lscpu | grep 'Socket(s)' | awk '{print $2}'")

    @staticmethod
    def init_cores():
        return produce_command("cat /proc/cpuinfo | grep '^processor' | wc -l")

    @staticmethod
    def init_speed():
        return produce_command("lscpu | grep 'CPU MHz' | awk '{print $3}'")

    @staticmethod
    def init_arch():
        return produce_command("lscpu | grep 'Arch' | awk '{print $2}'")