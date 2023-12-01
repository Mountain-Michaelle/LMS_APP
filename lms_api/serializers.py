from rest_framework import serializers
from . import models 


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = [
                  'id',
                  'full_name', 'email', 'mobile_no', 'profile_pix',
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
        'course_duration', 'time', 'course_chapters', 'related_course', 'total_enrolled_student'
      )
      


class CourseChapterSerializer(serializers.ModelSerializer):
   class Meta: 
      model = models.CourseChapter 
      fields = [
         'id', 'ref_course',  'title',  'video', 'remark', 'created', 'average_rating'
      ]
    
   def __init__(self, *args, **kwargs):
    super(CourseChapterSerializer, self).__init__(*args, **kwargs)
    request = self.context.get('request')
    self.Meta.depth = 0
    if request and request.method == 'GET':
      self.Meta.depth = 1

class CourseChapterSerializerGet(serializers.ModelSerializer):
   class Meta: 
      model = models.CourseChapter 
      fields = [
         'id', 'ref_course',  'title',   'remark', 'created', 'average_rating'
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
      

## // Student Registeration and functionalities

class StudentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Student
    fields = [
      'id', 'full_name', 'admission_letter', 'email', 'password', 'password2', 'qualification', 'interested_course'
    ]
    
    
class StudentErollSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.StudentCourseEnrollment
    fields = ['id', 'course', 'student', 'enrolled_time']
    

class EnrolledStudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.StudentCourseEnrollment
    fields = ['id', 'course', 'student', 'enrolled_time']
    depth=1

class CourseRatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.CourseRating
    fields = ['id', 'course', 'student', 'review', 'rating', 'rated_date']
  
  ## Overwriting the depth variable at post method, sets it zero and 1 at get method.
  def __init__(self, *args, **kwargs):
    super(CourseRatingSerializer, self).__init__(*args, **kwargs)
    request = self.context.get('request')
    self.Meta.depth = 0
    if request and request.method == 'GET':
      self.Meta.depth = 1
    

# Favorite course Serializers 
class StudentFavoriteCourseSerilizer(serializers.ModelSerializer):
  class Meta:
    model = models.StudentFavouriteCourse
    fields = ['id', 'course', 'student', 'status']
  
  def __init__(self, *args, **kwargs):
    super(StudentFavoriteCourseSerilizer, self).__init__(*args, **kwargs)
    request = self.context.get('request')
    self.Meta.depth = 0
    if request and request.method =='GET':
      self.Meta.depth = 2
      

class StudentAssignmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.StudentAssignment
    fields = ["id", "title", "detail", "documents", "teacher", "course"]
  
  def __init__(self, *args, **kwargs):
    super(StudentAssignmentSerializer, self).__init__(*args, **kwargs)
    request = self.context.get('request')
    self.Meta.depth = 0
    if request and request.method == 'GET':
      self.Meta.depth = 2
      
  

class StudentAssignmentSubmitSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.StudentAssignmentSubmission
    fields = ['student', 'course', 'answer', 'date', 'documents']