from rest_framework import serializers
from . import models 


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = [
                  'id',
                  'full_name', 'email', 
                  'password', 'password2', 'skills', 'postal_code', 'qualification', 'teacher_course'
                ]

class CourseCategorySerilizer(serializers.ModelSerializer):
  class Meta:
    model = models.CourseCategory
    fields = [
       'id',
      'title',
      'description'
    ]
    

   
class CourseListSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Course
      fields = (
        'id', 'category', 'topic', 'teacher', 'course_image', 'description', 
        'course_duration', 'time', 'course_chapters', 'related_course' 
      )
      


class CourseChapterSerializer(serializers.ModelSerializer):
   class Meta: 
      model = models.CourseChapter 
      fields = [
         'id', 'ref_course',  'title',  'video', 'remark', 'created',
      ]


# Views for the students pages 


class TeacherSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = [
                  'id', 'full_name', 'email', 'skills', 'postal_code', 
                  'qualification', 'teacher_course'
                ]

  
class CourseSerializer2(serializers.ModelSerializer):
   class Meta:
      model = models.Course
      fields = ('id', 'category', 'topic', 'teacher', 'course_image',  
        'course_duration', 'time', 'course_chapters', 'related_course' )
      depth=1