import json
from logging import getLogger

from Luke.MongoClient.MRequestList import MRequestList
from Luke.common.Status import Status
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Api import Api, logger
from Luke.MongoClient.MBareMetalList import MBareMetalList


def index(request):
    if request.method == "POST":
        r = request.POST.get("request")
    elif request.method == "GET":
        r = request.GET.get("request")
    else:
        r = "wow"
    return HttpResponse(str(r))


@csrf_exempt
@require_http_methods(["POST", "GET"])
def add_req(request):
    api = get_api()
    if request.method == "POST":
        result = api.handle_new_request(req=request)
    elif request.method == "GET":
        result = MRequestList().load_requests()
    return check_result(result)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def add_bm(request):
    api = get_api()
    result = api.handle_new_bare_metal(bare_metal=request)[1].id
    return check_result(result)


@csrf_exempt
@require_http_methods(["GET"])
def get_bm(request, bm_id):
    mb = MBareMetalList()
    result = mb.load_bare_metal(bm_id)
    return check_result(result)


@csrf_exempt
@require_http_methods(["POST"])
def update_status(request, bm_id):
    result = None
    mb = MBareMetalList()
    status = request.POST['status']
    if Status.is_status_valid(status):
        result = mb.update_status(status, bm_id)
    return check_result(result)


def check_result(result):
    if result:
        return HttpResponse(content=json.dumps(result), status=200)
    else:
        return HttpResponse(content="invalid request", status=500)


def get_api():
    app = get_wsgi_application()

    try:
        return app.api
    except AttributeError:
        app.__dict__['api'] = Api()
        return app.api
