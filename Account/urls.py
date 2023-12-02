from django.urls import path 
from .views import StudentSignUpView, TeacherSignupView, getCSRFToken, AccountDelete, \
    StudentLoginView, TeacherLoginView, LogoutView, GetStudentUsersProfileVeiw, GetTeacherUsersProfileVeiw, \
        UpdateStudentUserProfileView, UpdateTeacherUserProfile


urlpatterns = [
    ## Student Url
    path('student-register/', StudentSignUpView.as_view()),
    path('student-login/', StudentLoginView.as_view()),
    path('student-profile/', GetStudentUsersProfileVeiw.as_view()),
    path('student-profile-update/', UpdateStudentUserProfileView.as_view()),
    ## Teacher Url
    path('teacher-register/', TeacherSignupView.as_view()),
    path('teacher-login/', TeacherLoginView.as_view()),
    path('teacher-profile/', GetTeacherUsersProfileVeiw.as_view()),
    path('teacher-profile-update/', UpdateTeacherUserProfile.as_view()),
    
    #General
    path('logout/', LogoutView.as_view()),
    path('account-delete/', AccountDelete.as_view()),
    path('csrf-cookie/', getCSRFToken.as_view()),
]
