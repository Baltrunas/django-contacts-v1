from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.contacts, name='contacts'),
	url(r'^callback/$', views.callback, name='callback'),
]
