from django.shortcuts import render
from .models import About, StudentsMessages
# Create your views here.


def about(request):
    
    abouts= About.objects.all()
    studentmessages= StudentsMessages.objects.all()
    
    return render (request, "about.html", {'abouts': abouts, 'studentmessages': studentmessages})

  