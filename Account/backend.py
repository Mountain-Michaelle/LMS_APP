from django.contrib.auth.backends import ModelBackend
from .models import StudentUserProfile


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
    