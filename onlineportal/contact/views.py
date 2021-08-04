from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
   
from contact.forms import ContactForm
# Create your views here.

def contact(request):
    
    title = 'Contact Information'
    confirm_message = 'Do you have any Questions?'
    form = ContactForm(request.POST or None)
    context = {'title': title, 'confirm_message': confirm_message, 'form': form, }
    if form.is_valid():
        name = form.cleaned_data['name']
        content = form.cleaned_data['content']
        subject = 'Message from mysite.com'
        message = '%s %s ' %(content, name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
        title = "Thanks!"
        confirm_message = "Thanks for the message. We will get right back to you."
        context = {'title': title, 'confirm_message': confirm_message, }
    
    template = 'contact.html'
    return render(request, template, context)