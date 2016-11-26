from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^maplayer/$', views.map_layer_list, name='index'),
    url(r'^maplayer/(?P<floor>[0-9]+)/$', views.map_layer, name='index'),
    url(r'^navigate/$', views.navigate, name='index'),
    url(r'^edit_floor/$', views.editor, name='index'),
    url(r'^office/$', views.office_list, name='index'),
    url(r'^office/(?P<name>.*)$', views.office, name='index'),
    url(r'^iterate/$', views.iterate_step, name='index'),
    url(r'^create_route/$', views.create_route, name='index'),
    url(r'^scooters_data/$', views.scooters_data, name='index'),
    url(r'^add_scooters/$', views.add_scooters, name='index')
]
