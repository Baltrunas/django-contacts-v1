# -*- coding: utf-8 -*
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import SafeUnicode


class Subject(models.Model):
	title = models.CharField(max_length=512, verbose_name=_('Title'))
	email = models.CharField(max_length=128, verbose_name=_('E-Mail'))
	phone = models.CharField(max_length=32, verbose_name=_('Phone'))

	from_name = models.CharField(max_length=128, verbose_name=_('From name'))
	from_email = models.EmailField(max_length=128, verbose_name=_('From E-Mail'))

	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	class Meta:
		verbose_name = _('Subject')
		verbose_name_plural = _('Subjects')

	def __unicode__(self):
		return SafeUnicode('%s &rarr; %s' % (self.title, self.email))


class Mesage(models.Model):
	name = models.CharField(max_length=512, verbose_name=_('Name'))
	url = models.URLField(max_length=256, blank=True, null=True, verbose_name=_('URL'))
	phone = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('Phone'))
	email = models.EmailField(max_length=128, blank=True, null=True, verbose_name=_('E-Mail'))
	subject = models.ForeignKey(Subject, related_name='mesages', default=1, verbose_name=_('Subject'))
	msg = models.TextField(blank=True, null=True, verbose_name=_('Mesage'))
	ip = models.IPAddressField(blank=True, null=True, editable=False, verbose_name=_('IP'))
	STATUS_CHOICES = (
		('error', _('Error')),
		('send', _('Send')),
		('read', _('Read')),
	)
	status = models.CharField(verbose_name=_('Status'), max_length=32, choices=STATUS_CHOICES, editable=False)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return '#%s - %s from %s' % (self.pk, self.subject.title, self.name)

	class Meta:
		ordering = ['-updated_at']
		verbose_name = _('Mesage')
		verbose_name_plural = _('Mesages')
