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
   path('course-list/chapter/<int:pk>/', views.CourseChapterRating.as_view()),
   path('student/course/<int:id>/', views.CourseLIstView.as_view()),
   
   ##### These are the student phase of the apppliction routers ######
   path('student/list/create/', views.StudentListCreate.as_view()),
   path('student/login/', views.student__login, name="student-login"),
   path('student-enroll-course/', views.StudentEnrollmentView.as_view() ),
   #path('student-enroll-course/', views.CourseEnrolment.as_view()),
   path('student-enroll-course/<int:course_id>/<int:student_id>/', views.fetch_enrolled_student ),
   path('fetch-enrolled-student/<int:course_id>', views.EnrrolledStudentList.as_view()),
   path('fetched-enrolled-student/<int:course_id>/', views.FetchedEnrolledStudentLIst.as_view()),
   path('course-rating/<int:course_id>/', views.CourseRatingCreateView.as_view()),
   path('course-rating/chapter/<int:course_id>/', views.CourseRatingSingleView.as_view()),
   path('rating-status/', views.RatingStatus.as_view()),
   path('student-favorite-course/', views.StudentFavoriteCourseListView.as_view()),
   path('student-fav-course/', views.StudentFavCourse.as_view()),
   path('fetch-favorite-status/<int:student_id>/<int:course_id>/', views.fetch_favorite_course_status, name="fetch-favortie"),
   path('remove-favorite-course/<int:student_id>/<int:course_id>/', views.remove_favorite_course, name="remove-favorite"),
   path('student-assignment/<int:course_id>/<int:teacherId>/', views.StudentAssignmentView.as_view() ),
   path('student-assignment-detail/<int:pk>/', views.StudentAssignmentView.as_view() ),
   path('student-assignment-submit/<int:course_id>/<int:student_id/', views.StudentAssignmentSubmitView.as_view()),
]
