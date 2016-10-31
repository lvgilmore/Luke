import json
import threading

import time

from requests import get
from requests import post

from Luke.common.Status import Status


class PollingStatus(threading.Thread):
    """
        A thread class that run every 3 seconds and checks the status of baremetal
    """

    def __init__(self, port, bare_metal_id):
        threading.Thread.__init__(self)
        self.port = port
        self.bare_metal_id = bare_metal_id
        self.status = Status.nothing

    def run(self):
        while True:
            bm = get('http://localhost:{}/baremetal/{}'.format(self.port, self.bare_metal_id))
            # if baremetal found
            if bm.content:
                baremetal_status = int(json.loads(bm.content)['status'])
                print baremetal_status
                if self.status is not baremetal_status:
                    self.check_status(baremetal_status)

            time.sleep(3)

    def check_status(self, baremetal_status):
        print "old status: " + str(self.status)

        self.status = baremetal_status
        print "new status: " + str(self.status)

        # update status
        post('http://localhost:{}/baremetal/changestatus/{}/'.format(self.port, self.bare_metal_id),
            data={"status": str(self.status)})

        if self.status is Status.matched:
            print "status changed to matched"
        elif self.status is Status.reboot:
            print "status changed to reboot"
        elif self.status is Status.done:
            print "status changed to done"
        else:
            print "status is nothing"
