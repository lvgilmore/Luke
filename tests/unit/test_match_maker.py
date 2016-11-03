import os
import time
import unittest
import uuid

from Luke.Api import Api
from Luke.BareMetal import BareMetal
from requests import post

DELAY_SECONDS = 2
PORT = 8000


class TestMatchMaker(unittest.TestCase):
    def setUp(self):
        if 'LUKE_PATH' not in os.environ:
            os.environ['LUKE_PATH'] = os.path.join(os.path.dirname(__file__), "../../")

        self.api = Api()

    def tearDown(self):
        self.api.request_list.database['requests'].delete_many({})

    def test_no_request(self):
        """
        got new bare metal, no requests in file
        :return: no best match
        """
        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]

        self.assertEqual(best_request, None)

    def test_request_empty(self):
        """
        got new bare metal, no requests in file
        :return: no best match
        """
        req = "{}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req})
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]

        self.assertEqual(best_request, None)

    def test_no_match(self):
        """
        bare metal not match requirements
        :return:
        no best match found
        """
        req = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"2\",\
                                                  \"Speed\": \"333.000\", \"Cores\": \"6\"}," \
              "\"Vendor\": \"vend\"}," \
              "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
              "\"NICs\": {\"ens33\": " \
              "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                      \"Type\": \"Twisted Pair\"}}," \
              " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
              "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
              "\"Model\": \"mod\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req})
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]

        self.assertEqual(best_request, None)

    def test_no_requirements(self):
        """
        request with no requirements
        :return: request not in a valid format
        """
        req = "{\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
              "\"NICs\": {\"ens33\": " \
              "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                      \"Type\": \"Twisted Pair\"}}," \
              " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
              "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
              "\"Model\": \"mod\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req})
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]

        self.assertEqual(best_request, None)

    def test_match(self):
        """
        one request with requirements that match bare metal
        :return: request
        """
        req_id = str(uuid.uuid4())
        req = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
              "\"Vendor\": \"vend\"}," \
              "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
              "\"NICs\": {\"ens33\": " \
              "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
              \"Type\": \"Twisted Pair\"}}," \
              " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
              "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
              "\"Model\": \"mod\", \"profile\": \"common\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                     \"Type\": \"Twisted Pair\", \"ip\": \"192.168.0.4\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req, "request_id": req_id})
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]
        self.assertEqual(best_request.id, req_id)

    def test_match2(self):
        """
        more than one request in request file, one request match bare metal
        :return:
        """
        req_id1 = str(uuid.uuid4())
        req1 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
               "\"Vendor\": \"vend\"}," \
               "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
               "\"NICs\": {\"ens33\": " \
               "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
               \"Type\": \"Twisted Pair\"}}," \
               " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
               "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
               "\"Model\": \"mod\", \"profile\": \"common\"}}"

        req2 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
               "\"Vendor\": \"vend\"}," \
               "\"other_prop\": {\"Ram\": {\"Size\": \"1111111\"}, " \
               "\"NICs\": {\"ens33\": " \
               "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
               \"Type\": \"Twisted Pair\"}}," \
               " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
               "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
               "\"Model\": \"mod\", \"profile\": \"common\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"ip\": \"192.168.0.4\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req1, "request_id": req_id1})
        post("http://localhost:{}/request/".format(PORT), data={"request": req2})

        # response = post("http://localhost:{}/baremetal/".format(8000), data={"bare_metal": bare_metal})
        # self.assertEqual(response.text, req_id1)

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]
        self.assertEqual(best_request.id, req_id1)

    def test_match_by_time(self):
        """
        more than one request in request file, and more than one request match bare metal (same score)
        :return: request with highest creation time
        """
        req_id1 = str(uuid.uuid4())
        req1 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
               "\"Vendor\": \"vend\"}," \
               "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
               "\"NICs\": {\"ens33\": " \
               "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
               \"Type\": \"Twisted Pair\"}}," \
               " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
               "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
               "\"Model\": \"mod\", \"profile\": \"common\"}}"

        req_id2 = str(uuid.uuid4())
        req2 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
               "\"Vendor\": \"vend\"}," \
               "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
               "\"NICs\": {\"ens33\": " \
               "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
               \"Type\": \"Twisted Pair\"}}," \
               " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
               "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
               "\"Model\": \"mod\", \"profile\": \"common\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"ip\": \"192.168.0.4\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req1, "request_id": req_id1})
        time.sleep(DELAY_SECONDS)
        post("http://localhost:{}/request/".format(PORT), data={"request": req2, "request_id": req_id2})

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]
        self.assertEqual(best_request.id, req_id1)

    def test_match_by_time_middle_match(self):
        """
        request file contatins request(1) that dont match bare metal,
        comes new request(2) that match, later comes another request(3) that match
        :return: request with highest creation time(request2)
        """
        req1 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"2\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
               "\"Vendor\": \"vend\"}," \
               "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
               "\"NICs\": {\"ens33\": " \
               "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
               \"Type\": \"Twisted Pair\"}}," \
               " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
               "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
               "\"Model\": \"mod\", \"profile\": \"common\"}}"

        req_id = str(uuid.uuid4())
        req_match1 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                        \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     "\"Vendor\": \"vend\"}," \
                     "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                     \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\", \"profile\": \"common\"}}"

        req_match2 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                        \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     "\"Vendor\": \"vend\"}," \
                     "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
                     \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\", \"profile\": \"common\"}}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \"ip\": \"192.168.0.4\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req1})
        time.sleep(DELAY_SECONDS)
        post("http://localhost:{}/request/".format(PORT), data={"request": req_match1, "request_id": req_id})
        time.sleep(DELAY_SECONDS)
        post("http://localhost:{}/request/".format(PORT), data={"request": req_match2})

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]
        self.assertEqual(best_request.id, req_id)

    def test_baremetal_empty(self):
        """
        one request with requirements that match bare metal
        :return: request
        """
        req_id = str(uuid.uuid4())
        req = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
              "\"Vendor\": \"vend\"}," \
              "\"other_prop\": {\"Ram\": {\"Size\": \"3062784\"}, " \
              "\"NICs\": {\"ens33\": " \
              "{\"Speed\": \"1000Mb/s\", \"Mac\": \"00:0c:29:3d:5e:ce\", \
              \"Type\": \"Twisted Pair\"}}," \
              " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
              "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
              "\"Model\": \"mod\"}}"

        bare_metal = "{}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req, "request_id": req_id})
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]
        self.assertEqual(best_request, None)

    def test_request_not_valid(self):
        """
        one request with requirements that match bare metal
        :return: request
        """
        req_id = str(uuid.uuid4())
        req = "{\"Cpu\": \"Cpu\"}"

        bare_metal = "{\"Vendor\": \"vend\"," \
                     " \"Cpu\": {\"Sockets\": \"1\", \"Arch\": \"x86_64\", \
                     \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
                     " \"Ram\": {\"Size\": \"3062784\"}, " \
                     "\"NICs\": {\"ens33\": " \
                     "{\"Speed\": \"1000Mb/s\", \
                     \"Mac\": \"00:0c:29:3d:5e:ce\", \"Type\": \"Twisted Pair\"}}," \
                     " \"Disks\": {\"sda\": {\"Vendor\": \"VMware\", \"Size\": \"2\"}, " \
                     "\"sr0\": {\"Vendor\": \"VMware\", \"Size\": \"5\"}}, " \
                     "\"Model\": \"mod\"}"

        post("http://localhost:{}/request/".format(PORT), data={"request": req, "request_id": req_id})
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))[0]
        self.assertEqual(best_request, None)
