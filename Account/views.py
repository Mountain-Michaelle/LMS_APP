import datetime
from multiprocessing import AuthenticationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
## Verifications
from rest_framework import permissions, generics, status
from django.template.loader import render_to_string
from django.conf import settings
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
## ends
from . import models
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
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

@method_decorator(csrf_exempt, name='dispatch')
class StudentSignUpView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email').lower()
        re_password = data.get('re_password')
        reg_no = data.get('reg_no').lower()
        required_substrings = ['unn', 'imt', 'b.sc', '/']
        
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
                                return Response({"error": "This registration number is already linked to another user, please contact the management"})
                            else:
                                if models.StudentUserProfile.objects.filter(email=email).exists():
                                    return Response({"error": "Email already exists"})
                                else:
                                    user = User.objects.create_user(username=username, password=password)
                                    user.save()
                                    user = User.objects.get(id=user.id) 
                                    student_profile = models.StudentUserProfile(student=user, first_name='', last_name='',
                                                        phone='', country='', state='', email=email, postal='', reg_no=reg_no, hobbies='', is_student=True)
                                    student_profile.save()
                                    return Response({'success': 'Student acount created successfully!'})
                                    
                        else:
                            return Response({"error": f" You must provide your valid imt degree program registration number eg.' imt/unn/b.sc/cos/year/reg'. "}) 
            else:
                return Response({'error': 'passwords do not match'})
        except:
            return Response({"error": "Field Violation(s)"})
    
    

@method_decorator(csrf_exempt, name='dispatch')
class TeacherSignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        
        username = data['username']
        course = data['course']
        email = data['email']
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
                        if models.TeacherUserProfile.objects.filter(email=email).exists():
                            return Response({"error": "Email already exists"})
                        else:
                            user = User.objects.create_user(username=username, password=password)
                            user.save()

                            user = User.objects.get(id=user.id)
                            teacher_profile = models.TeacherUserProfile(teacher=user, is_teacher=True, phone='', country='', state='',
                                                                        postal='', course=course, hobbies='', email=email,)
                            teacher_profile.save()
                            return Response({"success": "Account created successfully"})
                        
                        
            else:
                return Response({'error': 'passwords do not match'})
        except:
            return Response({"error": "Something went wrong on teacher registration"})
    

# @method_decorator(csrf_exempt, name='dispatch')
# class getCSRFToken(APIView):
#     permission_classes = (permissions.AllowAny,)
#     def get(self, request, format=None):
#         return Response({'success': 'CSRF cookie set'}) 
    

@method_decorator(csrf_exempt, name='dispatch')
class StudentLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        reg_no = data.get('reg_no')
        password = data.get('password') 
        try:
            #reg = models.StudentUserProfile.objects.filter(reg_no=reg_no).lower()
            user = authenticate(request, reg_no=reg_no, password=password)
            
            if user is not None:
                if models.StudentUserProfile.objects.filter(is_student=False):
                    return Response({"Account disabled from the site, please contact the management"})
                else:
                    login(request, user)
                    return Response({'success': 'User authenticated'})
            else:
                return Response({"error": "Invalid credential(s)"})
        except:
            return Response({"error": "something went wrong"})
        
        
        
### Teacher login view
@method_decorator(csrf_exempt, name='dispatch')
class TeacherLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        
        try:
            email = data['email']
            password = data['password']
            user = auth.authenticate(request, email=email, password=password)
            
            if user is not None:
                if models.TeacherUserProfile.objects.filter(is_teacher=True):
                    auth.login(request, user)
                    return Response({'success': 'User authenticated'})
                else:
                    return Response({"error": "You are suspended from IMTech online, please contact the management"})
            else:
                return Response({"error": "Invalid password or email"})
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
@method_decorator(csrf_exempt, name='dispatch')
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
@method_decorator(csrf_exempt, name='dispatch')
class GetTeacherUsersProfileVeiw(APIView):
    def get(self, request, format=None):
        # try:
        user = self.request.user
        username = user.username
        user = User.objects.get(id=user.id)
        user_profile = models.TeacherUserProfile.objects.get(teacher=user)
        user_profile_serialized = TeacherUserSerializer(user_profile)
        return Response({"teacher_profile": user_profile_serialized.data, "username": str(username)})
        # except:  
        #     return Response({"error": "Error fetching data"})
            


## Student Profile Update View
@method_decorator(csrf_exempt, name='dispatch')
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
@method_decorator(csrf_exempt, name='dispatch')
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


#### Forgotten password Views
class StudentDetail(generics.RetrieveAPIView):
    queryset = models.StudentUserProfile.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class StudentList(generics.ListAPIView):
    queryset = models.StudentUserProfile.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = (permissions.AllowAny,)
    
class TeacherList(generics.ListAPIView):
    queryset = models.TeacherUserProfile.objects.all()
    serializer_class = TeacherUserSerializer
    permission_classes = (permissions.AllowAny,)
    

class TeacherDetail(generics.RetrieveAPIView):
    queryset = models.TeacherUserProfile.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
@method_decorator(csrf_exempt, name='dispatch')
class StudentSendCodeView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        data = self.request.data
        try:
            try:
                email = data.get('email')
                reg_no = data.get('reg_no').lower()
                student = models.StudentUserProfile.objects.get(email=email)  
                
                if models.StudentUserProfile.objects.filter(email=email, reg_no=reg_no).exists():
                    ## Clear the existing verification code in the database
                    if student:
                        student.verification_code=None
                        student.code_expiration = None
                        student.save()
                        
                        # Generate and send a new verification code in the database
                        # And generate new code at each request
                        code = ''.join(random.choices('0123456789', k=6))
                        email_body = render_to_string('password_reset_email.html', {'code': code})
                        expiration_time = timezone.now() + datetime.timedelta(minutes=10)
                        send_mail("password reset verification code", None,
                                settings.DEFAULT_FROM_EMAIL, [email],
                                html_message=email_body, 
                                fail_silently=False,
                                )
                        # store the code in the databse for later verification
                        student.verification_code = code
                        student.code_expiration = expiration_time
                        student.save()
                        return Response({"success": "Verification code sent successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error": "Invalid email"})
                else:
                    return Response({"error": "Invalid Registration number"})
                    
            except ObjectDoesNotExist:
                return Response({"error": "No Account matching query found"})
        except:
            return Response({"error": "Something went wrong, check your connection"})
        

@method_decorator(csrf_exempt, name='dispatch')
class StudentVerifyCodeView(APIView):
    permission_classes = (permissions.AllowAny,)   
    def post(self, request, format=None):
        data = self.request.data 
        try:
            email = data['email']
            code = data['code']  
            try:
                student = models.StudentUserProfile.objects.get(email=email)
            except student.DoesNotExist:
                return Response({"error": "User does not exist"})
            
            if not student.is_code_expired() and code == student.verification_code:
                if models.StudentUserProfile.objects.filter(email=email).exists():
                    if code == student.verification_code:
                        user = student.student
                        new_password = data['new_password']
                        re_new_password = data['re_new_password']
                        if not student.is_code_expired():
                            if new_password != re_new_password:
                                return Response({"error": "Passwords do not match"})
                            else:
                                if len(new_password) < 8:
                                    return Response({"error": "Passwords must be at least 8 characters"})
                                else:
                                    user.set_password(new_password)
                                    user.save()
                                    return Response({"success": "Password reset successful!"})
                        else:
                            return Response({'error': 'Expired code'})
                    else:
                        return Response({"error": "Invalid code"})
                else:
                    return Response({'error': "Invalid email or registraton number"})
            else:
                return Response({"error": "Expired or invalid registration code"})
        except:
            return Response({"error": "Something went wrong"})

@method_decorator(csrf_exempt, name='dispatch')
class TeacherSendCodeView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data 
        try:
            email = data["email"]
            teacher = models.TeacherUserProfile.objects.get(email=email)
            #Generate codes
            if teacher:
                teacher.verification_code = None 
                teacher.code_expiration = None
                teacher.save()
                
                code = ''.join(random.choices('0123456789ABCDEF', k=8))
                email_body = render_to_string('password_reset_email.html', {'code': code})
                expiration_time = timezone.now() + datetime.timedelta(minutes=10)
                # Store the code in database
                teacher.verification_code = code
                teacher.code_expiration = expiration_time
                teacher.save()
                
                send_mail("password reset verification code", None,
                            settings.DEFAULT_FROM_EMAIL, [email], html_message=email_body,
                            fail_silently=False) 
                return Response({"success": "Verification code sent successfully"})
            else:
                return Response({"error": "Not a registered email"})
        except:
            return Response({"error": "Wrong email or connection"})
        # except:
        #     return Response({"error": "Something went wrong"})
        
        
@method_decorator(csrf_exempt, name='dispatch')
class TeacherVerifyCodeView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        data = self.request.data
        email = data['email']
        re_new_password = data['re_new_password']
        new_password = data['new_password']
        code = data['code']
        teacher = models.TeacherUserProfile.objects.get(email=email)
        teacher_profile = models.TeacherUserProfile.objects.filter(email=email, verification_code=code)
        
        if not teacher.is_code_expired() and code == teacher.verification_code:
            if teacher:
                if teacher_profile.exists():
                    if code == teacher.verification_code:
                        if not teacher.is_code_expired():
                            if len(new_password) < 8:
                                return Response({"error": "Passwords must be at least 8 characters"})
                            else:
                                if new_password != re_new_password:
                                    return Response({"error": "Passwords do not match"})
                                else:
                                    user = teacher.teacher
                                    user.set_password(new_password)
                                    user.save()
                                    return Response({"success": "Password reset successful"})
                        else:
                            return Response({"error": "Expired code"})
                    else:
                        return Response({"error": "Invalid verification code"})
                else:
                    return Response({"error": "Invalid code"})
            
            else :
                return Response({"error": "Invalid Account" })
        else:
            return Response({'error': "Invalid or expired code"})
    