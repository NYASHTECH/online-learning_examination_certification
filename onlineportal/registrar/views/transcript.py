from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from classroom.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from classroom.models import CoursePreview
from classroom.models import Student
from classroom.models import Teacher
from classroom.models import Course
from registrar.models import CourseFinalMark
from registrar.models import CourseSetting
from registrar.forms import CourseForm


@login_required(login_url=settings.LOGIN_URL)
def transcript_page(request):
    courses = Course.objects.filter(status=settings.COURSE_AVAILABLE_STATUS)
    
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)

    try:
        marks = CourseFinalMark.objects.filter(student=student)
    except CourseFinalMark.DoesNotExist:
        marks = None

    return render(request, 'registrar/transcript/list.html',{
        'courses' : courses,
        'student' : student,
        'marks': marks,
        'user' : request.user,
        'tab' : 'transcript',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })