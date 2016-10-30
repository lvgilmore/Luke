"""automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Luke.views import *
from Luke.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^request', add_req, name='addReq'),
    url(r'^baremetal/$', add_bm, name='addBm'),
    url(r'^baremetal/(?P<bm_id>[-0-9a-z]+)/$', get_bm, name='getBm'),
    url(r'^baremetal/(?P<bm_id>[-0-9a-z]+)/?P<bm_status>[a-zA-z]/$',
        update_status, name='updateStatus'),
]
