from django.contrib import admin

from .models import Quiz,Question,Answer,Subject,Course,CoursePreview,LandpageTopPickCourse,Teacher,Student, SubSubject
from .models import LandpageContactMessage,LandpageCoursePreview,LandpagePartner,LandpageTeamMember,Profile

admin.site.register(Course)
admin.site.register(CoursePreview)
admin.site.register(LandpageTopPickCourse)
admin.site.register(LandpageContactMessage)
admin.site.register(LandpageCoursePreview)
admin.site.register(LandpagePartner)
admin.site.register(LandpageTeamMember)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Profile)


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Subject)
admin.site.register(SubSubject)


