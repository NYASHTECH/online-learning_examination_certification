from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
import random

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
 

class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class SubSubject(models.Model):
    sub_subject = models.CharField(max_length=250, blank=True, null=True)
    subject = models.ForeignKey(Subject,null=True, blank=True,
        verbose_name = "Subject", on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_subject + " (" + self.subject.name + ")"


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    sub_subjects = models.ForeignKey(SubSubject, on_delete=models.CASCADE, null=True, blank=True, related_name='subtopics')
    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name = "Random Order",
        help_text = "Display the questions in "
                    "a random order or as they "
                    "are set?")

    def __getquestions__(self):
        questions = []

        for _ in range(1,100):
           selection= random.randint(initial = 0,id=question.id)
           question = random.choice(selection)
           self.questions.append(question)

    def __str__(self):
        return self.name 

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)
    sub_subjects = models.ForeignKey(SubSubject, on_delete=models.CASCADE,blank=True,
                                     null=True, related_name ='sub_subjects')

    def __str__(self):
        return self.text 


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'at_teachers'


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')

COURSE_CATEGORY_TYPES = (
    ( 'Engineering  Design', 'Engineering  Design'),
    ( 'Welding Techniques', 'Welding Techniques'),
    ( 'Information Security', 'Information Security'),
    ( 'Business Management', 'Business Management'),
    ( 'Bio Pharmacy', 'Bio Pharmacy'),
    ('Information Technology',  'Information Technology'),
)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=127, choices=COURSE_CATEGORY_TYPES, default='General Education')
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    is_official = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=settings.COURSE_UNAVAILABLE_STATUS)
    image = models.ImageField(upload_to='uploads', null=True, blank=True)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(Course, self).delete(*args, **kwargs) # Call the "real" delete() method

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'at_courses'


class LandpageTeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    full_name = models.CharField(max_length=31)
    role = models.CharField(max_length=31)
    twitter_url = models.CharField(max_length=255, null=True)
    facebook_url = models.CharField(max_length=255, null=True)
    image_filename = models.CharField(max_length=255, null=True)
    linkedin_url = models.CharField(max_length=255, null=True)
    github_url = models.CharField(max_length=255, null=True)
    google_url = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'at_landpage_team_members'


class LandpageCoursePreview(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_landpage_course_previews'

class LandpageTopPickCourse(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.course.title
    
    class Meta:
        db_table = 'at_landpage_top_pick_courses'


class CoursePreview(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=63)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    description = models.TextField()
    summary = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_course_previews'


class LandpageContactMessage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    email = models.EmailField()
    phone = models.CharField(max_length=63)
    message = models.TextField()
    posted_date = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name + " " + self.email + " " + self.phone
    
    class Meta:
        db_table = 'at_landpage_contact_message'


class LandpagePartner(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=127)
    url = models.URLField()
    
    def __str__(self):
        return self.title + ' ' + self.url
    
    class Meta:
        db_table = 'at_landpage_partners'

class  Profile(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg', upload_to= 'profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self):
        super().save()
        img=Image.open(self.image.path)
        if img.height >300 or img.width >300 :
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
