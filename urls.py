# -*- coding: utf-8 -*
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('contact.views',
	# contacts
	url(r'^contacts/$', 'contacts', name='contacts'),
)
