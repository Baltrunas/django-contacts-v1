# -*- coding: utf-8 -*
from django import template
register = template.Library()

@register.filter
def getitem(item, string):
	try:
		return item.get(string, '')
	except:
		return ''
