import os
import time
import unittest
import uuid

from Luke.Api import Api
from Luke.BareMetal import BareMetal

DELAY_SECONDS = 2


class TestMatchMaker(unittest.TestCase):
    def setUp(self):
        self.api = Api()
        if 'LUKE_PATH' not in os.environ:
            os.environ['LUKE_PATH'] = os.path.join(os.path.dirname(__file__), "../../")

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

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))

        self.assertEqual(best_request, None)

    def test_request_empty(self):
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

        self.api.handle_new_request("{}")
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))

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

        self.api.handle_new_request(req)
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))

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

        self.api.handle_new_request(req)
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))

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

        self.api.handle_new_request(req, req_id)
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))
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
               "\"Model\": \"mod\"}}"

        req2 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
               "\"Vendor\": \"vend\"}," \
               "\"other_prop\": {\"Ram\": {\"Size\": \"1111111\"}, " \
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

        self.api.handle_new_request(req1, req_id1)
        self.api.handle_new_request(req2)

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))
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
               "\"Model\": \"mod\"}}"

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

        self.api.handle_new_request(req1, req_id1)
        time.sleep(DELAY_SECONDS)
        self.api.handle_new_request(req2, req_id2)

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))
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
               "\"Model\": \"mod\"}}"

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
                     "\"Model\": \"mod\"}}"

        req_match2 = "{\"requirements\": {\"Cpu\": {\"Sockets\": \"1\",\
                        \"Speed\": \"2201.000\", \"Cores\": \"1\"}," \
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

        self.api.handle_new_request(req1)
        time.sleep(DELAY_SECONDS)
        self.api.handle_new_request(req_match1, req_id)
        time.sleep(DELAY_SECONDS)
        self.api.handle_new_request(req_match2)

        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))
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

        self.api.handle_new_request(req, req_id)
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))
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

        self.api.handle_new_request(req, req_id)
        best_request = self.api.handle_new_bare_metal(BareMetal(bare_metal))
        self.assertEqual(best_request, None)
