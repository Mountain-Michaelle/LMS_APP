from django.utils import timezone
from django.db import models
from django.core import serializers

# Create your models here.

# Teacher Model
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    nationality = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=12, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name

# Course Category Model
class CourseCategory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Course Categories'
    def __str__(self):
        return self.title

# Course Model
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_course')
    topic = models.CharField(max_length=200)
    description = models.TextField()
    course_duration = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now=True)
    course_image = models.ImageField(upload_to='course_image/%Y/%m/%d/', default=None, blank=True, null=True)
    
    class Meta:
        verbose_name_plural="Courses"
    
    def related_course(self):
        related_course = Course.objects.filter(topic__icontains=self.topic)
        return serializers.serialize('json', related_course)

        
    def __str__(self):
        return self.topic
    

class CourseChapter(models.Model):
    ref_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='chapter_video/%Y/%m/%d/')
    remark = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self):
        return self.title.title()

     
     
     
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    address = models.TextField()
    interested_categories = models.TextField()

    def __str__(self, *arg):
        return self.full_name.split('', arg)


