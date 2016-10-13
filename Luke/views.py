from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Api import Api


def index(request):
    if request.method == "POST":
        r = request.POST.get("request")
        return HttpResponse(str(r))
    elif request.method == "GET":
        r = request.GET.get("request")
        return HttpResponse(str(r))
    return HttpResponse("wow")


@csrf_exempt
@require_http_methods(["POST", "GET"])
def add_req(request):
    api = get_api()
    # api.handle_new_request(request.POST.get("request"))

    # post_data = {'name': 'Gladys'}
    # response = request.post('http://example.com', data=post_data)
    # content = response.content
    # return HttpResponse(content)

    # send post request from some function
    # import requests
    # r = requests.post("http://127.0.0.1:8080/request")
    # if we want to send data:
    # r = requests.post("http://127.0.0.1:8080/request", data=post_data)
    # r.text

    if request.method == "POST":
        api.handle_new_request(request.POST.get("request"))
        return HttpResponse("good post")
    elif request.method == "GET":
        return HttpResponse("good get")


def get_api():
    app = get_wsgi_application()
    try:
        return app.api
    except AttributeError:
        app.__dict__['api'] = Api()
