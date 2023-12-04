from django.urls import path 
from .views import StudentSignUpView, TeacherSignupView, getCSRFToken, AccountDelete, \
    StudentLoginView, TeacherLoginView, LogoutView, GetStudentUsersProfileVeiw, GetTeacherUsersProfileVeiw, \
        UpdateStudentUserProfileView, UpdateTeacherUserProfile, StudentDetail, StudentSendCodeView, \
            StudentVerifyCodeView, TeacherSendCodeView, TeacherVerifyCodeView


urlpatterns = [
    ## Student Url
    path('student-register/', StudentSignUpView.as_view()),
    path('student-login/', StudentLoginView.as_view()),
    path('student-profile/', GetStudentUsersProfileVeiw.as_view()),
    path('student-profile-update/', UpdateStudentUserProfileView.as_view()),
    path('student-detail/<int:pk>/', StudentDetail.as_view()),
    ## Teacher Url
    path('teacher-register/', TeacherSignupView.as_view()),
    path('teacher-login/', TeacherLoginView.as_view()),
    path('teacher-profile/', GetTeacherUsersProfileVeiw.as_view()),
    path('teacher-profile-update/', UpdateTeacherUserProfile.as_view()),
    
    # General
    path('logout/', LogoutView.as_view()),
    path('account-delete/', AccountDelete.as_view()),
    path('csrf-cookie/', getCSRFToken.as_view()),
    
    ## Forgotten Password
    path('student-send-code-reset-passsword/', StudentSendCodeView.as_view()),
    path('student-verify-code-reset-password/', StudentVerifyCodeView.as_view()),
    
    ## Teacher section
    path('teacher-send-code-reset-password/', TeacherSendCodeView.as_view()),
    path('teacher-verify-code-reset-password/', TeacherVerifyCodeView.as_view())
    
    
]
