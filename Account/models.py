from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.
class StudentUserProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default="",  blank=True, null=True)
    last_name = models.CharField(max_length=255, default="",  blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20,  blank=True, null=True)
    country = models.CharField(max_length=200,  blank=True, null=True)
    state = models.CharField(max_length=30,  blank=True, null=True)
    reg_no = models.CharField(max_length=26, validators=[RegexValidator(regex=r'^[a-zA-Z]+/[a-zA-Z]+/[a-zA-Z]+\.[a-zA-Z]+/[a-zA-Z]+/\d{4}/\d{3}$',
                                                        message="Enter a valid registration number in the specified format")],
                              unique=True)
    postal = models.CharField(max_length=30,)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    is_student = models.BooleanField(default=True)
    
    def __str__(self):
        return self.first_name
    
class TeacherUserProfile(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=30)
    postal = models.CharField(max_length=20)
    course = models.CharField(max_length=255)
    hobbies = models.CharField(max_length=255)
    is_teacher = models.BooleanField(default=True)
    def __str__(self):
        return self.first_name
