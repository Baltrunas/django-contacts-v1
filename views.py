# -*- coding: utf-8 -*
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext

from contacts.models import Message
from contacts.models import CallBack
from contacts.models import Office

from contacts.forms import MessageForm
from contacts.forms import CallBackForm


def contacts(request):
	context = {}
	context['offices'] = Office.objects.all()

	if request.method == 'POST':
		context['form'] = MessageForm(request.POST)
		if context['form'].is_valid():
			context['formdate'] = context['form'].cleaned_data
			context['ip'] = request.META.get('REMOTE_ADDR', None)
			context['referer'] = request.META.get('HTTP_REFERER', None)
			email = context['formdate'].get('email', None)

			form_subject = context['formdate'].get('subject', None)
			context['form_subject'] = form_subject

			send_from = '%s <%s>' % (form_subject.from_name, form_subject.from_email)

			user_content = render_to_string('contacts/email_user.html', context)
			user_subject = _('We received your message!')
			sendmsg = EmailMultiAlternatives(user_subject, user_content, send_from, [email])
			sendmsg.attach_alternative(user_content, "text/html")
			sendmsg.send()

			admin_content = render_to_string('contacts/email_admin.html', context)
			sendmsg = EmailMultiAlternatives(form_subject.title, admin_content, send_from, [form_subject.email])
			sendmsg.attach_alternative(admin_content, "text/html")
			sendmsg.send()

			context['ok'] = True
			context['form'] = MessageForm()
			context['name'] = context['formdate'].get('name', None)
			Message(
				name=context['formdate'].get('name', None),
				phone=context['formdate'].get('phone', None),
				email=context['formdate'].get('email', None),
				url=context['formdate'].get('url', None),
				subject=context['formdate'].get('subject', None),
				msg=context['formdate'].get('msg', None),
				ip=request.META.get('REMOTE_ADDR', None),
				status='send'
			).save()
		else:
			context['formdate'] = context['form'].cleaned_data
			Message(
				name=context['formdate'].get('name', None),
				phone=context['formdate'].get('phone', None),
				email=context['formdate'].get('email', None),
				url=context['formdate'].get('url', None),
				subject=context['formdate'].get('subject', None),
				msg=context['formdate'].get('msg', None),
				ip=request.META.get('REMOTE_ADDR', None),
				status='error'
			).save()
	else:
		context['ok'] = False
		context['form'] = MessageForm()
	context['title'] = _('Contacts')
	return render_to_response('contacts/page.html', context, context_instance=RequestContext(request))


def callback(request):
	context = {}
	if request.method == 'POST':
		context['form'] = CallBackForm(request.POST)
		context['ip'] = request.META.get('REMOTE_ADDR', None)
		if context['form'].is_valid():
			context['formdate'] = context['form'].cleaned_data
			form_subject = context['formdate'].get('subject', None)
			context['form_subject'] = form_subject

			send_from = '%s <%s>' % (form_subject.from_name, form_subject.from_email)

			admin_content = render_to_string('contacts/email_callback.html', context)
			sendmsg = EmailMultiAlternatives(form_subject.title, admin_content, send_from, [form_subject.email])
			sendmsg.attach_alternative(admin_content, "text/html")
			sendmsg.send()

			context['ok'] = True
			context['form'] = MessageForm()
			context['name'] = context['formdate'].get('name', None)
			CallBack(
				salutation=context['formdate'].get('salutation', None),
				first_name=context['formdate'].get('first_name', None),
				last_name=context['formdate'].get('last_name', None),
				subject=context['formdate'].get('subject', None),
				phone=context['formdate'].get('phone', None),
				from_time=context['formdate'].get('from_time', None),
				to_time=context['formdate'].get('to_time', None),
				msg=context['formdate'].get('msg', None),
				ip=context['ip'],
				status='wait'
			).save()
		else:
			try:
				context['formdate'] = context['form'].cleaned_data
				CallBack(
					salutation=context['formdate'].get('salutation', None),
					first_name=context['formdate'].get('first_name', None),
					last_name=context['formdate'].get('last_name', None),
					subject=context['formdate'].get('subject', None),
					phone=context['formdate'].get('phone', None),
					from_time=context['formdate'].get('from_time', None),
					to_time=context['formdate'].get('to_time', None),
					msg=context['formdate'].get('msg', None),
					ip=context['ip'],
					status='error'
				).save()
			else:
				pass
	else:
		context['ok'] = False
		context['form'] = CallBackForm()
	context['title'] = _('Call Back')
	return render_to_response('contacts/callback.html', context, context_instance=RequestContext(request))
