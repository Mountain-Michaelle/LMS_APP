from django.shortcuts import render
from rest_framework.views import APIView
from .models import Teacher, Course, CourseCategory, CourseChapter
from .serializers import TeacherSerializer,CourseCategorySerilizer, CourseListSerializer, CourseChapterSerializer, CourseSerializer2, TeacherSerializer2
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import generics, viewsets
# Create your views here.

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    #permission_classes=[permissions.IsAuthenticated]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'pk'
    #permission_classes=[permissions.IsAuthenticated]

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
        navigate
    
class CourseCategoryList(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerilizer
    # Permission classes here  


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    # Permission class here
    
    # Usage of slice to get only some amount of course not all
    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = Course.objects.all().order_by('-id')[:limit]
        return qs


# Courses specific to a teacher
class TeacherCourse(generics.ListAPIView):
    serializer_class = CourseListSerializer
    
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)
        return Course.objects.filter(teacher=teacher)
    
class TeacherCourseDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()


class CourseChapterView(generics.ListCreateAPIView):
    queryset = CourseChapter.objects.all()
    serializer_class = CourseChapterSerializer
    

class CourseChapterList(generics.ListAPIView):
    serializer_class = CourseChapterSerializer
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        return CourseChapter.objects.filter(ref_course=course)

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
    
        
        