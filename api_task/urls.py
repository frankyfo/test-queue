from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api_task/$', views.api_task, name='api_task'),
    url(r'^api_task/(?P<id>[0-9]+)/$', views.api_status_task, name='api_status_task'),
    ] 