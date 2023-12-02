from multiprocessing import AuthenticationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from . import models
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.decorators import method_decorator
from .serializers import StudentUserSerializer, TeacherUserSerializer

# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class CheckIsAuthenticated(APIView):
    def get(self, request, format=None):
        isAuthenticated = User.is_authenticated
        try:
            if isAuthenticated:
                return Response({"isAuthenticated": "success"})
            else:
                return Response({"isAuthenticated": "error"})
        except:
            return Response({"error": "Error checking authentication status"})

@method_decorator(csrf_protect, name='dispatch')
class StudentSignUpView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data
        
        username = data['username']
        password = data['password']
        re_password = data['re_password']
        reg_no = data['reg_no']
        required_substrings = ['imt', 'unn', 'b.sc', '/']
    
        try: 
            if password == re_password: 
                if User.objects.filter(username=username).exists():
                    return Response({'error': f'A username with {username} already exists'})
                else:
                    if len(password) < 8:
                        return Response({'error': 'Passwords must be at least 8 characters'})
                    else:
                        if all(substrings.lower() in reg_no for substrings in required_substrings):
                            if models.StudentUserProfile.objects.filter(reg_no=reg_no).exists():
                                return Response({"error": "This Reg. No. is already registered by another user, please contact the management"})
                            else:
                                user = User.objects.create_user(username=username, password=password)
                                user.save()
                                user = User.objects.get(id=user.id) 
                                student_profile = models.StudentUserProfile(student=user, first_name='', last_name='',
                                                    phone='', country='', state='', postal='', reg_no=reg_no, hobbies='', is_student=True)
                                student_profile.save()
                                return Response({'success': 'Student acount created successfully!'})
                                
                        else:
                            return Response({"error": f"{reg_no} not valid, ensure the format follows the standard, eg.' imt/unn/b.sc/course/year/reg.number' all in lower cases"})   
            else:
                return Response({'error': 'passwords do not match'})
        except:
            return Response({"error": "Something went wrong on registration"})
    
    

@method_decorator(csrf_protect, name='dispatch')
class TeacherSignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        
        username = data['username']
        course = data['course']
        password = data['password']
        re_password = data['re_password']
        
        try:
            if password == re_password:
                if User.objects.filter(username=username).exists():
                    return Response({"error": f"A user with the user name {username} already exists"})
                else:
                    if len(password) < 8:
                        return Response({"error": "Passwords must be at least 8 characters"})
                    else:
                        user = User.objects.create_user(username=username, password=password)
                        user.save()

                        user = User.objects.get(id=user.id)
                        teacher_profile = models.TeacherUserProfile(teacher=user, is_teacher=True, phone='', country='', state='',
                                                                    postal='', course=course, hobbies='', email='',)
                        teacher_profile.save()
                        return Response({"success": "Account created successfully"})
                    
                        
            else:
                return Response({'error': 'passwords do not match'})
        except:
            return Response({"error": "Something went wrong on teacher registration"})
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
class getCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'}) 
    

@method_decorator(ensure_csrf_cookie, name='dispatch')
class StudentLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        
        reg_no = data['reg_no']
        password = data['password']
        reg = models.StudentUserProfile.objects.filter(reg_no=reg_no)
        user = authenticate(request, reg_no=reg_no, password=password)
        try:
            if user is not None:
                if models.StudentUserProfile.objects.filter(is_student=False):
                    return Response({"Account disabled from the site, please contact the management"})
                else:
                    login(request, user)
                    return Response({'success': 'User authenticated'})
            else:
                return Response({"error": "Invalid credential"}, status=401)
        except:
            return Response({"error": "something went wrong while logging in"})
        
        
        
### Teacher login view
@method_decorator(ensure_csrf_cookie, name='dispatch')
class TeacherLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        username = data['username']
        password = data['password']
        
        user = auth.authenticate(username=username, password=password)
        try:
            if user is not None:
                if models.TeacherUserProfile.objects.filter(is_teacher=False):
                    return Response({"error": "This account is temporarily suspended, please contact the management urgently"})
                else:
                    auth.login(request, user)
                    return Response({'success': 'User authenticated'})
            else:
                return Response({"error": "Invalid username or password"})
        except: 
            return Response({"error": "Something went wrong on teacher login"})

### Account logout view
class LogoutView(APIView):
    def post(self, request, format=None):
        
        try: 
            auth.logout(request)
            return Response({"success": "Loggout Out"})
        except:
            return Response({"error": "Loggout Failed"})
    
## Account deletion
class AccountDelete(APIView):
    def delete(self, request, format=None):
        
        try: 
            user = self.request.user
            user = User.objects.filter(id=user.id).delete()
            return Response({'success': 'User deleted successfully'})
        except:
            return Response({'error': 'Something went wrong'})
        
## Fetch Student Profile View
class GetStudentUsersProfileVeiw(APIView):
    def get(self, request, format=None):
        try:
            
            user = self.request.user
            username = user.username
            user = User.objects.get(id=user.id)
            user_profile = models.StudentUserProfile.objects.get(student=user)
            user_profile_serialized = StudentUserSerializer(user_profile)
            return Response({"student_profile": user_profile_serialized.data, "username": str(username)})
        except:
            return Response({"error": "Error fetching data"}) 

### Fetch Teacher Profile View
class GetTeacherUsersProfileVeiw(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            user = User.objects.get(id=user.id)
            user_profile = models.TeacherUserProfile.objects.get(teacher=user)
            user_profile_serialized = TeacherUserSerializer(user_profile)
            return Response({"teacher_profile": user_profile_serialized.data, "username": str(username)})
        except:
            return Response({"error": "Error fetching data"})
            


## Student Profile Update View
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UpdateStudentUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username 
            
            data = self.request.data
            first_name = data["first_name"]
            last_name = data["last_name"]
            phone = data["phone"]
            country = data["country"]
            state = data["state"]
            postal = data["postal"]
            email = data["email"]
            hobbies = data["hobbies"]
            
            user = User.objects.get(id=user.id)
            models.StudentUserProfile.objects.filter(student=user).update(
                first_name=first_name, last_name=last_name, phone=phone, country=country,
                state=state, postal=postal, email=email, hobbies=hobbies
            )
            user_profile = models.StudentUserProfile.objects.get(student=user)
            user_profile_serialized = StudentUserSerializer(user_profile)
            
            return Response({"student_profile": user_profile_serialized.data, "username": str(username)}) 
        except:
            return Response({"error": "Something went wrong while updating"})
    
    
## Teacher Profile Update view
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UpdateTeacherUserProfile(APIView):
    def put(self, request, format=None):
        try:
                
            user = self.request.user
            username = user.username 
            
            data = self.request.data
            first_name = data["first_name"]
            last_name = data["last_name"]
            phone = data["phone"]
            country = data["country"]
            state = data["state"]
            postal = data["postal"]
            email = data["email"]
            hobbies = data["hobbies"]
            
            user = User.objects.get(id=user.id)
            models.TeacherUserProfile.objects.filter(teacher=user).update(
                first_name=first_name, last_name=last_name, phone=phone, country=country,
                state=state, postal=postal, email=email, hobbies=hobbies
            )
            user_profile = models.TeacherUserProfile.objects.get(teacher=user)
            user_profile_serialized = TeacherUserSerializer(user_profile)
            
            return Response({"teacher_profile": user_profile_serialized.data, "username": str(username)}) 
        except:
            return Response({"error": "Something went wrong while updating"})