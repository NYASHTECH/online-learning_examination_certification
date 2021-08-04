from django.db import models
from classroom.models import Course

# Create your models here.
class About(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='pictures')
    name = models.CharField(max_length=300)
    satisfied_students = models.IntegerField()
    courses_offered = models.IntegerField()
    expert_advisors = models.IntegerField()
    schools = models.IntegerField()

class StudentsMessages(models.Model):
    image=models.ImageField(upload_to='student_messages')
    description=models.TextField()
    student_name =models.CharField(max_length=200)
    coursename =models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.coursename.title 