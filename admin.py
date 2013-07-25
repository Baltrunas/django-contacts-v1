# -*- coding: utf-8 -*
from django.contrib import admin

from contacts.models import Subject
from contacts.models import Message
from contacts.models import CallBack

from contacts.models import Region
from contacts.models import Office

from django.contrib.sites.models import Site


class SubjectAdmin(admin.ModelAdmin):
	list_display = ['title', 'email', 'created_at', 'updated_at']
	search_fields = ['title', 'email', 'created_at', 'updated_at']
	list_filter = ['email']
	ordering = ['title']

admin.site.register(Subject, SubjectAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name', 'salutation', 'phone', 'email', 'url', 'status', 'msg', 'ip', 'updated_at')
	search_fields = ('id', 'first_name', 'last_name', 'salutation', 'phone', 'email', 'url', 'status', 'msg', 'ip', 'updated_at')
	list_filter = ['updated_at', 'status']
	ordering = ['-updated_at']

admin.site.register(Message, MessageAdmin)


class CallBackAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'subject', 'phone', 'from_time', 'to_time', 'ip', 'status']
	search_fields = ['first_name', 'last_name', 'subject', 'phone', 'from_time', 'to_time', 'ip', 'status']
	list_filter = ['subject', 'phone', 'from_time', 'to_time', 'ip', 'status']
	ordering = ['-updated_at']

admin.site.register(CallBack, CallBackAdmin)


def __unicode__(self):
	return self.name

Site.__unicode__ = __unicode__


class RegionAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'code')
	search_fields = ('name', 'slug', 'code')

admin.site.register(Region, RegionAdmin)


class OfficeAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'address', 'order', 'public', 'main')
	search_fields = ('name', 'sites', 'email', 'address', 'order', 'public', 'main')
	list_editable = ['order', 'public', 'main']
	list_filter = ['public', 'main']

admin.site.register(Office, OfficeAdmin)
