from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext

from .models import Office

from .forms import MessageForm
from .forms import CallBackForm


def contacts(request):
	context = {}
	host = request.META.get('HTTP_HOST')
	context['offices'] = Office.objects.filter(public=True, sites__domain__in=[host])

	if request.method == 'POST':
		context['form'] = MessageForm(request.POST)
		if context['form'].is_valid():
			context['object'] = context['form'].save()
			context['object'].ip = context['ip'] = request.META.get('REMOTE_ADDR', None)
			context['referer'] = request.META.get('HTTP_REFERER', None)

			context['form_subject'] = context['object'].subject
			send_from = '%s <%s>' % (context['form_subject'].from_name, context['form_subject'].from_email)

			# Send User E-Mail
			try:
				user_subject = _('We received your message!')
				user_email_tpl = render_to_string('contacts/email_user.html', context)
				sendmsg = EmailMultiAlternatives(user_subject, user_email_tpl, send_from, [context['object'].email])
				sendmsg.attach_alternative(user_email_tpl, "text/html")
				sendmsg.send()
			except:
				pass

			# Send Admin E-Mail
			try:
				admin_email_tpl = render_to_string('contacts/email_admin.html', context)
				sendmsg = EmailMultiAlternatives(context['form_subject'].title, admin_email_tpl, send_from, [context['form_subject'].email])
				sendmsg.attach_alternative(admin_email_tpl, "text/html")
				sendmsg.send()
			except:
				pass

			context['ok'] = True
			context['form'] = MessageForm()
	else:
		context['ok'] = False
		context['form'] = MessageForm()
	context['title'] = _('Contacts')
	return render_to_response('contacts/page.html', context, context_instance=RequestContext(request))


def callback(request):
	context = {}
	if request.method == 'POST':
		context['form'] = CallBackForm(request.POST)
		if context['form'].is_valid():
			context['object'] = context['form'].save()
			context['object'].ip = context['ip'] = request.META.get('REMOTE_ADDR', None)

			context['form_subject'] = context['object'].subject
			send_from = '%s <%s>' % (context['form_subject'].from_name, context['form_subject'].from_email)

			# Send E-Mail
			try:
				admin_content = render_to_string('contacts/email_callback.html', context)
				sendmsg = EmailMultiAlternatives(context['form_subject'].title, admin_content, send_from, [context['form_subject'].email])
				sendmsg.attach_alternative(admin_content, "text/html")
				sendmsg.send()
			except:
				pass

			context['ok'] = True
			context['form'] = MessageForm()
	else:
		context['ok'] = False
		context['form'] = CallBackForm()
	context['title'] = _('Call Back')
	return render_to_response('contacts/callback.html', context, context_instance=RequestContext(request))
