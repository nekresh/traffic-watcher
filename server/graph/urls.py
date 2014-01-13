from django.conf.urls import *
import graph.views

urlpatterns = patterns('graph',
	url(r'^$', graph.views.index),
)
