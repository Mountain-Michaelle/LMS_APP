from django.contrib import admin
from .models import TeacherUserProfile, StudentUserProfile
# Register your models here.

admin.site.register(TeacherUserProfile)
admin.site.register(StudentUserProfile)