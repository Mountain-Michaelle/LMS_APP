from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentUserProfile, TeacherUserProfile


class CaseInsensitiveCustomRegField(serializers.CharField):
    def to_internal_value(self, data):
        return data.lower()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class StudentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    reg_no = CaseInsensitiveCustomRegField()
    class Meta:
        model = StudentUserProfile
        fields = ("id", "user", "email", "reg_no", "student", "first_name", "last_name", "is_student", "phone",
                  "country", "state", "postal",  "hobbies")

class TeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherUserProfile
        fields = ("teacher", "first_name", "last_name", "is_teacher", "phone", "country",
                  "state", "course", "postal", "course", "hobbies", "email",)
        
        