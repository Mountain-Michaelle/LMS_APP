from django.contrib.auth.backends import ModelBackend
from .models import StudentUserProfile, TeacherUserProfile
from django.contrib.auth.models import User

## Reg number sign up overriding.
class CustomBackend(ModelBackend):
    def authenticate(self, request, reg_no=None, password=None, **kwargs):
        try:
            student_profile = StudentUserProfile.objects.get(reg_no=reg_no)
        except StudentUserProfile.DoesNotExist:
            return None
        
        user = student_profile.student
        
        if user.check_password(password):
            return user 
        return None
    
    
class CustomTeaherAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            teacher_profile = TeacherUserProfile.objects.get(email=email)
        except TeacherUserProfile.DoesNotExist:
            return None 
        
        user = teacher_profile.teacher
        
        if user.check_password(password):
            return user
        return None