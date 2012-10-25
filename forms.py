# -*- coding: utf-8 -*-
from django.forms.widgets import Input
from django import forms
from django.utils.translation import ugettext as _
from django.forms import ModelForm
from contacts.models import Mesage


class Html5EmailInput(Input):
	input_type = 'email'
	required = 'required'


class Html5URLInput(Input):
	input_type = 'url'
	required = 'required'


class MesageForm(ModelForm):
	class Meta:
		model = Mesage


class ContactForm(forms.Form):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'required': 'required'}))
	tel = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'required': 'required'}))
	email = forms.EmailField(max_length=200, widget=Html5EmailInput(attrs={'required': 'required', 'placeholder': 'Электронная почта *'}))
	url = forms.CharField(required=False, max_length=200, widget=Html5URLInput())
	SERVICE_CHOICES = (
		('promo', _('Promo site')),
		('context', _('Context ads')),
		('make', _('Make site')),
	)
	service = forms.MultipleChoiceField(required=False, choices=SERVICE_CHOICES, widget=forms.widgets.CheckboxSelectMultiple)

	msg = forms.CharField(required=False, widget=forms.Textarea())

	# def clean_message(self):
		# message = self.cleaned_data['message']
		# num = len(message.split())
		# if num < 4:
			# raise forms.ValidationError('Слишком мало слов =(')
		# return message
