from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User, Profile)


from datetime import date
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import LandpageContactMessage


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'sub_subjects')


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = LandpageContactMessage
        fields = ['name','email', 'phone', 'message']
        labels = {
        }
        widgets = {
            'name': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Full Name'}),
            'email': EmailInput(attrs={'class': u'form-control','placeholder': u'Enter Email'}),
            'phone': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Phone'}),
            'comment': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Comment'}),
    }
    

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', None)
        
        # clean phone by removing all non-numerals
        phone = ''.join(x for x in phone if x.isdigit())
        
        ph_length = str(phone)
        min_length = 10
        max_length = 13
        if len(ph_length) < min_length:
            raise ValidationError('Must be 10 digit phone number.')
        if len(ph_length) > max_length:
            raise ValidationError('Must be at maxium 13 digits long')
        return phone


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
    )
    captcha = CaptchaField()

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email']
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']   