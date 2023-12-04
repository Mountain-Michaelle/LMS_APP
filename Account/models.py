from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError 
from django.utils import timezone
import re
# Create your models here.

class CustommRegField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 26)
        kwargs.setdefault('unique', True)
        super().__init__(*args, **kwargs)
    
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not self.is_valid_format(value):
            raise ValidationError('Invalid registration number format.')
    
    def is_valid_format(self, value):
        pattern = r'^[a-zA-Z]+/[a-zA-Z]+/[a-zA-Z]+\.[a-zA-Z]+/[a-zA-Z]+/\d{4}/\d{3}$'
        return bool(re.match(pattern, value))
    

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        return value.lower()


class StudentUserProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default="",  blank=True, null=True)
    last_name = models.CharField(max_length=255, default="",  blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20,  blank=True, null=True)
    country = models.CharField(max_length=200,  blank=True, null=True)
    state = models.CharField(max_length=30,  blank=True, null=True)
    reg_no = CustommRegField()
    postal = models.CharField(max_length=30, blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    is_student = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    code_expiration = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean() # validate before saving
        super().save(*args, **kwargs)
    
    def is_code_expired(self):
        return self.code_expiration is None or self.code_expiration < timezone.now()
        
    def __str__(self):
        return self.first_name
    
class TeacherUserProfile(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=30)
    postal = models.CharField(max_length=20)
    course = models.CharField(max_length=255)
    hobbies = models.CharField(max_length=255)
    is_teacher = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    code_expiration = models.DateTimeField(blank=True, null=True)
    
    def is_code_expired(self):
        return self.code_expiration is None or self.code_expiration < timezone.now()
    
    def __str__(self):
        return self.first_name
