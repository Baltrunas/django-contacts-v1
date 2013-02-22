# -*- coding: utf-8 -*
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('contacts.views',
	# contacts
	url(r'^$', 'contacts', name='contacts'),
	url(r'^callback/$', 'callback', name='callback'),
)
