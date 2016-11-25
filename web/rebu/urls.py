from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^maplayer/$', views.map_layer_list, name='index'),
    url(r'^maplayer/(?P<floor>[0-9]+)/$', views.map_layer, name='index'),
    url(r'^navigate/$', views.navigate, name='index'),
]
