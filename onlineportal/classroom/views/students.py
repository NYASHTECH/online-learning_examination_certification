from django.contrib import messages
import random
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.conf import settings

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm
from ..models import Quiz, Student, TakenQuiz, User
import os
import sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import smtplib 
import csv 


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
                with transaction.atomic():
                    student_answer = form.save(commit=False)
                    student_answer.student = student
                    student_answer.save()
                    if student.get_unanswered_questions(quiz).exists():
                        return redirect('students:take_quiz', pk)
                    else:
                        correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                        score = round((correct_answers / total_questions) * 100.0, 2)
                        TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                        if score < 50.0:
                            messages.warning(request, 'Better luck next time! Your mark for the Test %s is %s.' % (quiz.name, score))
                        else:
                            messages.success(request, 'Congratulations! You have completed the Test %s with success! You scored %s marks.' % (quiz.name, score))
                        return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })


@login_required(login_url=settings.LOGIN_URL)
def certificate(request):

    receiver = Student.objects.get(user=request.user)
    print(receiver)
  
    img = Image.open("media/certificates/templatecertificate.png")
    rgb= Image.new('RGB', img.size, (255, 255, 255))
    rgb.paste(img, mask=img.split()[3])
    # Load font
    font = ImageFont.truetype("arial.ttf", 60)
    draw = ImageDraw.Draw(rgb)
    draw.text((500,650), str(receiver) ,(40,40,40), font=font, )


    path="media/certificates/"

    rgb.save(path + str(receiver) +'.pdf',"PDF", resolution=100.0)

    with open(f"{path + str(receiver) +'.pdf'}",'rb' ) as pdf:
        response = HttpResponse(pdf.read(), content_type="application/vnd.pdf")
        response['Content-Disposition'] ='atttachment;filename=certificate.pdf'
        return response

    #return render(request, 'classroom/certificate/certificate_detail.html',{'new_path': ''})