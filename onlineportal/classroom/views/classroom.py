from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views.generic import TemplateView,ListView
from django.core import serializers

from classroom.models import LandpageTeamMember
from classroom.models import LandpageTopPickCourse
from classroom.models import LandpageCoursePreview
from classroom.models import CoursePreview
from classroom.models import LandpageContactMessage
from classroom.models import LandpagePartner
from classroom.models import Course
from classroom.forms import ContactForm
from django.contrib import messages
from django.db.models import Q


import json
from django.http import HttpResponse
from django.conf import settings

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    context = {
        'top_courses': LandpageTopPickCourse.objects.all(),
        'course_previews' : LandpageCoursePreview.objects.all(),
        'courses' : Course.objects.all(),
        'team_members' : LandpageTeamMember.objects.all().order_by('id'),
        'partners': LandpagePartner.objects.all(),
        'contact_form': ContactForm(),
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.AGENCY_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.AGENCY_JS_LIBRARY_URLS
    }
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:quiz_change_list')
        else:
            return redirect('students:quiz_list')
    return render(request, 'classroom/home.html', context)

class HomeView(ListView):
    model = Course
    template_name = 'classroom/home.html'

def course_preview_modal(request):
    course = None
    if request.is_ajax():
        if request.method == 'POST':
            POST = request.POST
            course_id = POST.get('course_id')
            if course_id is not None:
                try:
                    course = Course.objects.get(id=int(course_id))
                except Course.DoesNotExist:
                    pass
        return render(request, 'classroom/course_preview.html',{
            'course' : course
    })

def save_contact_us_message(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with sending message'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                form = ContactForm(request.POST)
            
                # Validate the form: the captcha field will automatically
                # check the input
                if form.is_valid():
                    name = request.POST['name']
                    email = request.POST['email']
                    phone = request.POST['phone']
                    message = request.POST['message']
                
                    # Save our message.
                    LandpageContactMessage.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        message=message,
                    ).save()
                    response_data = {'status' : 'success', 'message' : 'saved'}
                else:
                    response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
            except:
                response_data = {
                    'status' : 'failure',
                    'message' : 'could not save message ' + name + ' ' + email + ' ' + phone + ' ' + message
                }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def Search(request):
    if request.method=='POST':
        query =  request.POST['q']

        if query:
            courses = Course.objects.filter(

                Q(title__icontains=courses) |
                Q(description__icontains=courses)
            )

            if courses:
                return render(request, 'search.html', {'courses': courses})

            else:
                messages.error(request, "No result found")
        else:
            return HttpResponseRedirect("/search")

    return render(request, 'search.html')





    
 