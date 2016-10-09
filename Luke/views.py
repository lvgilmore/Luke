from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

from Api import Api


def index(request):
    if request.method == "POST":
        r = request.POST.get("request")
        return HttpResponse(str(r))
    elif request.method == "GET":
        r = request.GET.get("request")
        return HttpResponse(str(r))
    return HttpResponse("wow")


def addReq(request):
    api = get_api()
    api.handle_new_request(request.POST.get("request"))


def get_api():
    app = get_wsgi_application()
    try:
        return app.api
    except AttributeError:
        app.__dict__['api'] = Api()