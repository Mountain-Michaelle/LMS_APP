from django.urls import path 
from . import views

urlpatterns = [
   path('teachers/', views.TeacherList.as_view() ),
   # Login in the browsable django API 
   path('teachers/<int:pk>/', views.TeacherDetail.as_view()),
   path('teacher-login/', views.teacher_login, name='teacher-login'),
   path('course-category/', views.CourseCategoryList.as_view(), name="course-category"),
   path('courses/', views.CourseList.as_view(), name="courses"),
   # // Teacher Course
   path('teacher-course/<int:teacher_id>/', views.TeacherCourse.as_view(), name="teacher-course"),
   # // Teacher Course Detail and will enhance the delete
   path('courses/<int:pk>/', views.TeacherCourseDetails.as_view(), name='teacher-course'),
   
   path('chapter/', views.CourseChapterView.as_view(), name='chapter'),
   path('chapter/<int:course_id>/', views.CourseChapterList.as_view()),
   path('chapter/<int:pk>/edit', views.CourseChapterDetails.as_view()),
   path('student/courses/<int:pk>/', views.TeacherAndCourseDetails.as_view()),
   #path('student/course/<int:id>/', views.CourseLIstView.as_view()),
   
   ##### These are the student phase of the apppliction routers ######
   path('student/list/', views.StudentListCreate.as_view()),
   path('student/login/', views.student__login, name="student-login"),
   path('student-enroll-course/', views.StudentEnrollmentView.as_view() ),
   path('student-enroll-course/<int:course_id>/<int:student_id>/', views.fetch_enrolled_student ),
]
