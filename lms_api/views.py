from django.shortcuts import render
from rest_framework.views import APIView
from .models import (Teacher, Course, CourseCategory, CourseChapter, Student, StudentCourseEnrollment,
                    CourseRating, StudentFavouriteCourse, StudentFavouriteCourse, StudentAssignment, StudentAssignmentSubmission)
                    
from .serializers import TeacherSerializer,CourseCategorySerilizer, \
    CourseListSerializer, CourseChapterSerializer, CourseSerializer2, \
    StudentCreateSerializer, StudentErollSerializer, EnrolledStudentSerializer, CourseRatingSerializer, \
    CourseChapterSerializerGet, StudentFavoriteCourseSerilizer, StudentAssignmentSerializer, StudentAssignmentSubmitSerializer
from rest_framework.response import Response
from lms_api.models import Course
from lms_api.models import Student
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework import generics, viewsets
from Account.models import TeacherUserProfile, StudentUserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    #permission_classes=[permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'pk'

@csrf_exempt
def teacher_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:  
        teacher_data = Teacher.objects.filter().get(email=email, password=password)
        
    except Teacher.DoesNotExist:
        teacher_data = None
        
    if teacher_data:
        return JsonResponse({'login': True, 'teacher_id': teacher_data.id,
                             'teacher_name': teacher_data.full_name, 'teacher_course': teacher_data.skills})
    else:
        return JsonResponse({'login': False})
    
@method_decorator(csrf_exempt, name="dispatch")
class CourseCategoryList(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerilizer
    # Permission classes here  

@method_decorator(csrf_exempt, name="dispatch")
class CourseList(generics.ListCreateAPIView):
    #queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    # Permission class here
    # Usage of slice to get only some amount of course not all
    def get_queryset(self):
        # qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            return Course.objects.all().order_by('-id')[:limit]
       


# Courses specific to a teacher
class TeacherCourse(generics.ListAPIView):
    serializer_class = CourseListSerializer
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = User.objects.get(id=teacher_id)
        return Course.objects.filter(teacher=teacher)
    
class TeacherCourseDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()

@method_decorator(csrf_exempt, name="dispatch")
class CourseChapterView(generics.ListCreateAPIView):
    queryset = CourseChapter.objects.all()
    serializer_class = CourseChapterSerializer
    

class CourseChapterList(generics.ListAPIView):
    serializer_class = CourseChapterSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        return CourseChapter.objects.filter(ref_course=course)
    
class CourseChapterRating(generics.RetrieveAPIView):
    serializer_class = CourseChapterSerializerGet
    queryset = CourseChapter.objects.all()

class CourseChapterDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseChapterSerializer
    queryset = CourseChapter.objects.all()
    

class CourseLIstView(generics.ListAPIView):
    serializer_class = CourseSerializer2
    queryset = Course.objects.all()
    
    
class TeacherAndCourseDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer2
    lookup_field = 'pk'
    queryset = Course.objects.all()
    
    
###### These are all about student registrations and its functionalities ##### 
@method_decorator(csrf_exempt, name="dispatch")
class StudentListCreate(generics.ListCreateAPIView):
    serializer_class = StudentCreateSerializer
    queryset = Student.objects.all()
    

@csrf_exempt
def student__login(request):
    email = request.POST['email']
    password = request.POST['password']
    
    try:
        student_data = Student.objects.filter().get(email=email, password=password)
    except Student.DoesNotExist:
        student_data = None
        
    
    if student_data:
        return JsonResponse({
            'login': True, 'student_id': student_data.id })
    else:
        return JsonResponse({'login': False})     


@method_decorator(csrf_exempt, name="dispatch")

class StudentEnrollmentView(generics.ListCreateAPIView):
    serializer_class = StudentErollSerializer
    queryset = StudentCourseEnrollment.objects.all()

def fetch_enrolled_student(request, course_id, student_id):
    student = User.objects.filter(id=student_id).first()
    course = Course.objects.filter(id=course_id).first()
    studentEnrol = StudentCourseEnrollment.objects.filter(student=student).count()
    enrolledStatus = StudentCourseEnrollment.objects.filter(course=course, student=student).count()
    if enrolledStatus:
        return JsonResponse({'enrolled':True, 'studentEnrol':studentEnrol})  
    else:
        return JsonResponse({'enrolled': False})

class CourseEnrolment(APIView):
    
    def post(self, request, format=None):
        data = self.request.data
        student_id = data['student']
        course_id = data['course']
        user = self.request.user
        
        if User.objects.filter(id=student_id).exists():
            course_instance = get_object_or_404(Course, pk=course_id)
            student_instance = get_object_or_404(User, pk=student_id)
            is_active = User.objects.filter(id=student_id).exists()
            print(is_active)
            print(f'{course_id} \n')
            
            enrolled_course = StudentCourseEnrollment(course=course_instance, student=student_instance)
            enrolled_course.save()
            return Response({"success": "Course enrolment is successful"})
        else:
            return Response({"error": "User does not exists"})
        

class EnrrolledStudentList(generics.ListAPIView):
    queryset=StudentCourseEnrollment.objects.all()
    serializer_class = StudentErollSerializer
    
    def get__query(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        return StudentCourseEnrollment.objects.filter(course=course)
    
    
class FetchedEnrolledStudentLIst(generics.ListAPIView):
    #queryset = StudentCourseEnrollment.objects.order_by('enrolled_time')
    serializer_class = EnrolledStudentSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        return StudentCourseEnrollment.objects.filter(course=course)
    
class CourseRatingCreateView(generics.ListCreateAPIView):
    serializer_class = CourseRatingSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = CourseChapter.objects.get(pk=course_id)
        return CourseRating.objects.filter(course=course)

class CourseRatingSingleView(generics.ListAPIView):
    serializer_class = CourseRatingSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        print("course id ", course_id)
        course = CourseChapter.objects.get(id=course_id)
        return CourseRating.objects.filter(course=course)
    
    
## Fetching rating status Views, using a function based view

# def fetch_rating_status(request, student_id, course_id):
#     student = User.objects.filter(id=student_id).first()
#     course = CourseChapter.objects.filter(id=course_id).first()
#     ratingStatus = CourseRating.objects.filter(course=course, student=student).count()
    
#     if ratingStatus:
#         return JsonResponse({'hasRated': True})
#     else:
#         return JsonResponse({'hasRated': False})


@method_decorator(csrf_exempt, name="dispatch")
class RatingStatus(APIView):
    def post(self, request, format=None):
        data = self.request.data
        
        studentId = data['studentId']
        course_id = data['course_id']
        
        student = User.objects.filter(id=studentId).first()
        course = CourseChapter.objects.filter(id=course_id).first()
        ratingStatus = CourseRating.objects.filter(course=course, student=student).count()
        
        if ratingStatus:
            return JsonResponse({'hasRated': True})
        else:
            return JsonResponse({'hasRated': False})
        
        
### Add Favourite
class StudentFavoriteCourseListView(generics.ListCreateAPIView):
    queryset = StudentFavouriteCourse.objects.order_by('-course')
    serializer_class =  StudentFavoriteCourseSerilizer
    
class StudentFavCourse(APIView):
    def post(self, request, format=None):
        data = self.request.data
        studentId = data['studentId']
        student = User.objects.get(pk=studentId)
        queryset = StudentFavouriteCourse.objects.filter(student=student)
        queryset_serialized = StudentFavoriteCourseSerilizer(queryset)
        
        return Response(queryset_serialized.data)


## Remove Favourite;

def fetch_favorite_course_status(request, student_id, course_id):
    student = Student.objects.filter(id=student_id).first()
    course = CourseChapter.objects.filter(id=course_id).first()
    favoriteStatus = StudentFavouriteCourse.objects.filter(course=course, student=student).first()
    
    if favoriteStatus and favoriteStatus.status == True:
        return JsonResponse({"favorite": True})
    else:
        return JsonResponse({"favorite": False})


def remove_favorite_course(request, course_id, student_id):
    student = Student.objects.filter(id=student_id).first()
    course = CourseChapter.objects.filter(id=course_id).first()
    favoriteStatus = StudentFavouriteCourse.objects.filter(course=course, student=student).delete()
    if favoriteStatus:
        return JsonResponse({"favorite": True})
    else:
        return JsonResponse({"favorite": False})
    

class StudentAssignmentView(generics.ListCreateAPIView):
    #queryset = StudentAssignment.objects.order_by('-date')
    serializer_class = StudentAssignmentSerializer 
    def get_queryset(self):
        teacher_id = self.kwargs['teacherId']
        course_id = self.kwargs['course_id']
        teacher = Teacher.objects.get(id=teacher_id)
        course = Course.objects.get(pk=course_id)
        return StudentAssignment.objects.filter(teacher=teacher, course=course)
    

class StudentAssignmentView(generics.RetrieveAPIView):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer
    lookup_field = 'pk'

class StudentAssignmentSubmitView(generics.ListCreateAPIView):
    #queryset = StudentAssignmentSubmission.objects.order_by('-date')
    serializer_class = StudentAssignmentSubmitSerializer
    def get_queryset(self):
        student_id = self.kwargs['studentId']
        course_id = self.kwargs['course_id']
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(pk=course_id)
        return StudentAssignment.objects.filter(student=student, course=course)