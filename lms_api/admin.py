from django.contrib import admin
from .models import Teacher, Course, CourseCategory, Student, CourseChapter, StudentCourseEnrollment, CourseRating,\
    StudentFavouriteCourse, StudentAssignment, StudentAssignmentSubmission

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(CourseChapter)
admin.site.register(CourseCategory)
admin.site.register(Student)
admin.site.register(StudentCourseEnrollment)
admin.site.register(CourseRating)
admin.site.register(StudentFavouriteCourse)
admin.site.register(StudentAssignment)
admin.site.register(StudentAssignmentSubmission)