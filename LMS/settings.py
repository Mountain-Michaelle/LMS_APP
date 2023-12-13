"""
Django settings for LMS project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c07asg6nwkrxeo-6cq96t8_5mhxrt4la4ei2dhn^l((_)mh%pb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lms_api',
    'Account',
    'rest_framework', 
    "corsheaders",
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build'), os.path.join(BASE_DIR, "Account", 'build1')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#  'default': {
#      'ENGINE': 'django.db.backends.sqlite3',
#      'NAME': BASE_DIR / 'db.sqlite3',
#  }
#  }
   #   'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'mysql',
#     'USER': 'root',
#     'PASSWORD': 'Urbanus42',
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     }
      
    

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_test10',
        'USER': 'postgres',
        'PASSWORD': '41240075',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'staugustineimtmail@gmail.com'
EMAIL_HOST_PASSWORD = 'iedcoohcmthdtlkt'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Token Authentication setting for the Django app
REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.AllowAny']
} 

# 425853f593bbd978a43ff532bcf01aa66bef0a2a
## This is my authentication token for nemelu

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000"
]

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES' : [
#         'rest_framework.permissions.IsAuthenticated'
#     ],
#     'DEFAULT_AUTHENTICATION_CLASSES' : [
#         # 'rest_framework.authentication.SessionAuthentication'
#     ]
# }

## Custom Reg. Number login overriding
AUTHENTICATION_BACKENDS = [
    'Account.backend.CustomBackend',
    'Account.backend.CustomTeaherAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:8000" ]
