from django.utils import timezone
from django.db import models
from django.core import serializers

# Create your models here.

# Teacher Model
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    nationality = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=12, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    profile_pix = models.FileField(upload_to='teacher_pix/%Y/%m/%d/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Teachers"
    
    def skill_list(self):
        skill_list=self.skills.split(",")
        return skill_list
    
    ### Total Teacher Course
    def total_teacher_course(self):
        total_course = Course.objects.filter(teacher=self).count()
        return total_course
    
    ### Total Teacher Chapter
    def total_teacher_chapter(self):
        total_chapters=CourseChapter.objects.filter(course__teacher=self).count()
        return total_chapters
    
    def total_teacher_students(self):
        total_students = Student.objects.filter(course__teacher=self).count()
        return total_students
    

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
    
    def total_enrolled_student(self):
        total_enrolled_student = StudentCourseEnrollment.objects.filter(course=self).count()
        return total_enrolled_student
    
    def average_rating(self):
        average_rating = CourseRating.objects.filter(course=self).aggregate(models.Avg('rating'))
        return  average_rating
        
    def __str__(self):
        return self.topic
    

class CourseChapter(models.Model):
    ref_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='chapter_video/%Y/%m/%d/')
    remark = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=timezone.now)
    
    def average_rating(self):
        average_rating = CourseRating.objects.filter(course=self).aggregate(models.Avg('rating'))
        return  average_rating
        
    def __str__(self):
        return self.title.title()
    

     
     
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    admission_letter = models.FileField(upload_to='admission_letter/%Y/%m/%d/')
    reg_no = models.CharField(max_length=200, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    interested_course = models.TextField()

    def __str__(self, *arg):
        return self.full_name

class StudentCourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_courses')
    student  = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolled_student')
    enrolled_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural ="Enrolled Courses"


class CourseRating(models.Model):
    course = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='rated_courses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='rated_student')
    rating = models.PositiveIntegerField(default=1)
    review = models.TextField(max_length=211, null=True, blank=True)
    rated_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.course}-{self.student} rates => {self.rating}'
    

# Course Favorite functionality
class StudentFavouriteCourse(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural="7. Student Favorite Course"
    
    def __str__(self):
        return f"{self.course} => {self.student}"
    
    
class StudentAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    detail = models.TextField()
    documents = models.FileField(upload_to='student/assignments', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class StudentAssignmentSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    documents = models.FileField(upload_to="student/assignments/submission", null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.full_name} submited on {self.date}"