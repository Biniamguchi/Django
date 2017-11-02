from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^session/delete$', views.logout),
	url(r'^travels$', views.travels),	
	url(r'^travels/new$', views.new_travel),
	url(r'^create/(?P<id>\d+)$', views.create),
	url(r'^join/(?P<id>\d+)$', views.join),
	url(r'^leave/(?P<number>\d+)$', views.leave)
	# url(r'^/create/new/(?P<id>\d+)$', views.join),
	# url(r'^home/new$', views.home),
]

