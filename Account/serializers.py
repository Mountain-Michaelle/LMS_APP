from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentUserProfile, TeacherUserProfile



class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUserProfile
        fields = ("student", "first_name", "last_name", "reg_no", "is_student", "phone",
                  "country", "state", "postal",  "hobbies", "email",)

class TeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherUserProfile
        fields = ("teacher", "first_name", "last_name", "is_teacher", "phone", "country",
                  "state", "course", "postal", "course", "hobbies", "email",)
        
        