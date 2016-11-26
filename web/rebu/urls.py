from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^maplayer/$', views.map_layer_list, name='index'),
    url(r'^maplayer/(?P<floor>[0-9]+)/$', views.map_layer, name='index'),
    url(r'^navigate/$', views.navigate, name='index'),
    url(r'^edit_floor/$', views.editor, name='index'),
    url(r'^office/$', views.office_list, name='index'),
    url(r'^office/(?P<name>.*)$', views.office, name='index'),
    url(r'^debug_start/$', views.debug_start, name='index'),
    url(r'^debug_count/$', views.debug_count, name='index'),
]
