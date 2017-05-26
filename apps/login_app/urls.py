from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/process$', views.register_process),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^show$', views.show),
    url(r'^delete/(?P<id>\d+)$', views.delete)
]