import json
import threading
import time

from Luke.Api import logger
from Luke.common.Status import Status
from requests import get
from requests import post

SLEEP_SEC = 3


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
                baremetal_status = str(json.loads(bm.content)['status'])
                logger.debug("baremetal status from server is : " + baremetal_status)
                # check if status changed
                if self.status != baremetal_status:
                    self.update_status(baremetal_status)
            time.sleep(SLEEP_SEC)

    def update_status(self, baremetal_status):
        valid = True

        if baremetal_status == Status.matched:
            # change status to be something else
            self.status = Status.reboot
            print "status changed to matched"
        elif baremetal_status == Status.reboot:
            # change status to be something else
            self.status = Status.done
        elif baremetal_status == Status.done:
            # change status to be something else
            self.status = Status.nothing
        else:
            valid = False
            logger.debug("unknown baremetal status: " + baremetal_status + " was passed")

        if valid:
            logger.debug("baremetal new status is: " + self.status)

            # update status
            post('http://localhost:{}/baremetal/{}/status/'.format(self.port, self.bare_metal_id),
                data={"status": str(self.status)})
