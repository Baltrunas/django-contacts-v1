# -*- coding: utf-8 -*
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site


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
		return self.title


class Message(models.Model):
	name = models.CharField(max_length=512, verbose_name=_('Name'))
	url = models.URLField(max_length=256, blank=True, null=True, verbose_name=_('URL'), editable=False)
	phone = models.CharField(max_length=32, verbose_name=_('Phone'))
	email = models.EmailField(max_length=128, verbose_name=_('E-Mail'))
	subject = models.ForeignKey(Subject, related_name='messages', default=1, verbose_name=_('Subject'))
	msg = models.TextField(blank=True, null=True, verbose_name=_('Message'))
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
		verbose_name = _('Message')
		verbose_name_plural = _('Messages')


class CallBack(models.Model):
	SALUTATION_CHOICES = (
		('mr', _('Mr.')),
		('ms', _('Mis.')),
	)
	salutation = models.CharField(verbose_name=_('Salutation'), max_length=32, choices=SALUTATION_CHOICES)
	first_name = models.CharField(max_length=128, verbose_name=_('First Name'))
	last_name = models.CharField(max_length=128, verbose_name=_('Last Name'))
	subject = models.ForeignKey(Subject, related_name='callbacks', default=1, verbose_name=_('Subject'))
	phone = models.CharField(max_length=32, verbose_name=_('Phone'))
	from_time = models.TimeField(verbose_name=_('From Time'))
	to_time = models.TimeField(verbose_name=_('To Time'))
	msg = models.TextField(blank=True, null=True, verbose_name=_('Message'))

	ip = models.IPAddressField(blank=True, null=True, editable=False, verbose_name=_('IP'))
	STATUS_CHOICES = (
		('wait', _('Wait')),
		('in_process', _('In Process')),
		('error', _('Error')),
		('rejected', _('Rejected')),
		('finish', _('Finish')),
	)
	status = models.CharField(verbose_name=_('Status'), max_length=32, choices=STATUS_CHOICES)
	note = models.TextField(blank=True, null=True, verbose_name=_('Note'))
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return '#%s - %s from %s %s' % (self.pk, self.subject.title, self.last_name, self.first_name)

	class Meta:
		ordering = ['-updated_at']
		verbose_name = _('Call Back')
		verbose_name_plural = _('Call Backs')


class Region(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=128)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128, help_text=_('A slug is the part of a URL which identifies a page using human-readable keywords'))
	code = models.PositiveIntegerField(verbose_name=_('Code'), default=500)

	TYPE_CHOICES = (
		('city', _('City')),
		('state', _('State')),
		('country', _('Country')),
		('region', _('Region')),
	)
	region_type = models.CharField(verbose_name=_('Status'), max_length=32, choices=TYPE_CHOICES)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = _('Region')
		verbose_name_plural = _('Regions')


class Office(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=128)
	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

	phone = models.CharField(verbose_name=_('Phone'), max_length=64, default='+7 (000) 000-00-00', blank=True, null=True)
	email = models.CharField(verbose_name=_('E-mail'), max_length=128, default='email@mail.com', blank=True, null=True)
	address = models.CharField(verbose_name=_('Address'), max_length=2048, blank=True)

	www = models.URLField(verbose_name=_('WWW'), max_length=64, default='http://glav.it/', blank=True, null=True)

	photo = models.ImageField(verbose_name=_('Photo'), upload_to='img/office', blank=True)

	# страны
	# штат
	# города
	# регионы
	# city = models.ForeignKey(Region, verbose_name=_('City'), limit_choices_to={'region_type': 'city'})

	# параметры
	#	имя
	#	значение
	#	тип

	sites = models.ManyToManyField(Site, related_name='offices', verbose_name=_('Sites'))

	latitude = models.DecimalField(verbose_name=_('Latitude'), max_digits=19, decimal_places=15, blank=True, null=True)			# Широта
	longitude = models.DecimalField(verbose_name=_('Longitude'), max_digits=19, decimal_places=15, blank=True, null=True)		# Долгота

	order = models.PositiveSmallIntegerField(verbose_name=_('Order'), default=500)
	main = models.BooleanField(verbose_name=_('Main'), default=True)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def get_latitude(self):
		return '%s' % self.latitude

	def get_longitude(self):
		return '%s' % self.longitude

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['order', 'name']
		verbose_name = _('Office')
		verbose_name_plural = _('Offices')
