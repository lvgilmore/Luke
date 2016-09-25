import uuid

from Luke.Api import Api
import unittest

from Luke.BareMetal import BareMetal
from Luke.Request import Request
from Luke.matchMaker.MatchMaker import MatchMaker
from Luke.utils import JsonUtils


class TestMatchMaker(unittest.TestCase):
    def setUp(self):
        self.api = Api()

    def test_1(self):
        """
        got new bare metal, no requests in file
        :return:
        """
        best_request = self.api.handle_new_bare_metal(BareMetal("{\"name\": \"name1\","
                                                                " \"id\": \"id1\","
                                                                " \"os\": \"os\"}"))

        self.assertEqual(best_request, None)

    def test_2(self):
        """
        one request in requests file that not match the bare metal
        :return:
        """

    def test_3(self):
        """
        more than one request in requests file, but only one of requests match bare metal
        :return:
        """

    def test_4(self):
        """
        more than one request in requests file, but no one of them match bare metal
        :return:
        """

    def test_5(self):
        """
        more than one request in request file, and more than one request match bare metal
        :return:
        """

    def test_9(self):
        """
        request with no requirements, but with other_prop and os
        :return:
        """

        bare_metal = ("{\"name\": \"name\","
                      " \"id\": \"id1\","
                      " \"os\": \"Linux\"}")

        req_id = str(uuid.uuid4())
        request = Request("{\"other_prop\": {\"name\": \"name\","
                          " \"id\": \"id1\"},"
                          " \"os\": \"Linux\"}", req_id)
        api = Api()
        api.handle_new_request(request)
        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal)

        # read all requests from a file
        req_list = JsonUtils.read_json_from_file()

        m = MatchMaker()
        res = m.find_match_by_requirements(json_bare_metal,
                                           req_list)

        self.assertEquals(res[0].id, req_id)

    def test_10(self):
        """
        request with requirements, but without other_prop
        :return:
        """

        bare_metal = ("{\"name\": \"name\"," \
                      " \"id\": \"id1\"," \
                      " \"os\": \"Linux\"}")

        req_id = str(uuid.uuid4())
        request = Request("{\"requirements\": {\"name\": \"name\"," \
                          " \"id\": \"id1\"}," \
                          " \"os\": \"Linux\"}", req_id)
        api = Api()
        api.handle_new_request(request)
        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal)

        # read all requests from a file
        req_list = JsonUtils.read_json_from_file()

        m = MatchMaker()
        res = m.find_match_by_requirements(json_bare_metal,
                                           req_list)

        self.assertEquals(res[0].id, req_id)

    def test_6(self):
        """
        request with: no requirements, no other_prop
        :return:
        """
        bare_metal = ("{\"name\": \"name\","
                      " \"id\": \"id1\","
                      " \"os\": \"Linux\"}")

        req_id = str(uuid.uuid4())
        request = Request("{\"os\": \"Linux\"}", req_id)
        api = Api()
        api.handle_new_request(request)
        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal)

        # read all requests from a file
        req_list = JsonUtils.read_json_from_file()

        m = MatchMaker()
        res = m.find_match_by_requirements(json_bare_metal,
                                           req_list)

        self.assertEquals(res[0].id, req_id)

    def test_7(self):
        """
        request with requirements that dont match bare metal
        :return:
        """
        bare_metal = ("{\"name\": \"name\","
                      " \"id\": \"id1\","
                      " \"os\": \"os\"}")

        req_id = str(uuid.uuid4())
        request = Request("{\"requirements\": {\"name\": \"somename\"," \
                          " \"id\": \"id1\"}," \
                          " \"os\": \"Linux\"}", req_id)
        api = Api()
        api.handle_new_request(request)
        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal)

        # read all requests from a file
        req_list = JsonUtils.read_json_from_file()

        m = MatchMaker()
        res = m.find_match_by_requirements(json_bare_metal,
                                           req_list)

        self.assertEquals(res.__len__(), 0)

    def test_8(self):
        """
        request with requirements that fully match bare metal
        :return:
        """
        bare_metal = ("{\"name\": \"name\"," \
                      " \"id\": \"id1\"," \
                      " \"os\": \"os\"}")

        req_id = str(uuid.uuid4())
        request = Request("{\"requirements\": {\"name\": \"name\"," \
                          " \"id\": \"id1\"}," \
                          " \"os\": \"Linux\"}", req_id)
        api = Api()
        api.handle_new_request(request)
        json_bare_metal = JsonUtils.convert_from_json_to_obj(
            bare_metal)

        # read all requests from a file
        req_list = JsonUtils.read_json_from_file()

        m = MatchMaker()
        res = m.find_match_by_requirements(json_bare_metal,
                                           req_list)

        self.assertEquals(res[0].id, req_id)
