import json
import threading
import time
import os

from requests import get
from requests import post

from Luke.common.Status import Status


class PollingStatus(threading.Thread):
    """
        A thread class that run every 3 seconds and checks the status of baremetal
    """

    def __init__(self, uri, bare_metal_id):
        threading.Thread.__init__(self)
        self.uri = uri
        self.bare_metal_id = bare_metal_id
        self.status = Status.nothing

    def run(self):
        while True:
            bm = get('{}/baremetal/{}'.format(self.uri, self.bare_metal_id))
            # if baremetal found
            if bm.content:
                baremetal = json.loads(bm.content)
                baremetal_status = int(baremetal['status'])
                print baremetal_status
                if self.status is not baremetal_status:
                    self.check_status(baremetal_status, baremetal)

            time.sleep(3)

    def check_status(self, baremetal_status, baremetal):
        print "old status: " + str(self.status)

        self.status = baremetal_status
        print "new status: " + str(self.status)

        # update status
        post('{}/baremetal/changestatus/{}/'.format(self.uri, self.bare_metal_id),
            data={"status": str(self.status)})

        if self.status is Status.matched:
            if 'aciton' in baremetal:
                if baremetal['action'] == 'run':
                    os.system(baremetal['run_command'])
                self.status = 'reboot'
            else:
                print "status changed to matched"
        elif self.status is Status.reboot:
            print "status changed to reboot"
        elif self.status is Status.done:
            print "status changed to done"
        else:
            print "status is nothing"
