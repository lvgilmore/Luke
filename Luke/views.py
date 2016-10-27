from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Api import Api
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
        result = api.handle_new_request(request.POST.get("request"))
        if result:
            return HttpResponse(content=result, status=200)
        else:
            return HttpResponse(content="invalid request", status=500)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def add_bm(request):
    api = get_api()
    result = api.handle_new_bare_metal(request=request)
    if result:
        return HttpResponse(content=result, status=200)
    else:
        return HttpResponse(content="invalid request", status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_bm(request, bm_id):
    mb = MBareMetalList()
    # change the load func to receive id
    result = mb.load_bare_metal(bm_id)
    if result:
        return HttpResponse(content=result, status=200)
    else:
        return HttpResponse(content="invalid request", status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_status(request, bm_status):
    mb = MBareMetalList()
    result = mb.update_status(bm_status)
    if result:
        return HttpResponse(content=result, status=200)
    else:
        return HttpResponse(content="invalid request", status=500)


def get_api():
    app = get_wsgi_application()
    try:
        return app.api
    except AttributeError:
        app.__dict__['api'] = Api()
