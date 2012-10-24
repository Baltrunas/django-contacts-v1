# -*- coding: utf-8 -*
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from django.core.mail import EmailMultiAlternatives
# from django.utils.html import strip_tags
from django.template import RequestContext
from contact.models import Mesage
from contact.models import Subject
from contact.forms import MesageForm

context = {}


def contacts(request):
	if request.method == 'POST':
		context['form'] = MesageForm(request.POST)
		if context['form'].is_valid():
			context['formdate'] = context['form'].cleaned_data
			context['ip'] = request.META.get('REMOTE_ADDR', None)
			context['referer'] = request.META.get('HTTP_REFERER', None)
			email = context['formdate'].get('email', None)

			form_subject = Subject.object.get(pk=context['formdate'].get('subject', 1))

			send_from = '%s <%s>' % (form_subject.name, form_subject.email)

			user_content = render_to_string('contact/email_user.html', context)
			sendmsg = EmailMultiAlternatives('Мы получили вашу заявку!', user_content, send_from, [email])
			sendmsg.attach_alternative(user_content, "text/html")
			sendmsg.send()

			admin_content = render_to_string('contact/email_admin.html', context)
			sendmsg = EmailMultiAlternatives(form_subject.title, admin_content, send_from, [form_subject.email])
			sendmsg.attach_alternative(admin_content, "text/html")
			sendmsg.send()

			context['ok'] = True
			context['form'] = MesageForm()
			context['name'] = context['formdate'].get('name', None)
			context['title'] = 'Спасибо'

			Mesage(
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
			Mesage(
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
		context['form'] = MesageForm()
		context['title'] = _('Contacts')
	return render_to_response('contact/page.html', context, context_instance=RequestContext(request))
