# -*- coding: utf-8 -*-
from django.forms.widgets import Input
from django import forms
from django.utils.translation import ugettext as _
from django.forms import ModelForm
from contacts.models import Message
from contacts.models import CallBack


class Html5EmailInput(Input):
	input_type = 'email'
	required = 'required'


class Html5URLInput(Input):
	input_type = 'url'
	required = 'required'


class MessageForm(ModelForm):
	salutation = forms.TypedChoiceField(
		label=_('Salutation'),
		coerce=lambda x: True if x == 'True' else False,
		initial=False,
		choices=((False, _('Mrs.')), (True, _('Mr.'))),
		widget=forms.RadioSelect
	)

	class Meta:
		model = Message


class CallBackForm(ModelForm):
	class Meta:
		model = CallBack
		fields = ['subject', 'salutation', 'first_name', 'last_name', 'from_time', 'to_time', 'phone', 'msg']


class ContactForm(forms.Form):
	name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'required': 'required'}))
	phone = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'required': 'required'}))
	email = forms.EmailField(max_length=200, required=True, widget=Html5EmailInput(attrs={'required': 'required', 'placeholder': 'email@example.com'}))
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
