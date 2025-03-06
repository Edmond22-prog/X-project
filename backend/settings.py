'''
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
'''
import datetime
from pathlib import Path

from envparse import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7d3-+or0l!an*5js2(gj!w(gyq6w(fl_6mfp*a!dzt1^0q)9&k'

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
    'app_models',
    'endpoints',
    'drf_yasg',
    'rest_framework',
    'rest_framework_jwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': f'{env("POSTGRES_DB_NAME", "project_db")}',
        'USER': f'{env("POSTGRES_DB_USER", "user")}',
        'PASSWORD': f'{env("POSTGRES_DB_PASSWORD", "password")}',
        'HOST': f'{env("POSTGRES_DB_HOST", "127.0.0.1")}',
        'PORT': f'{env("POSTGRES_DB_PORT", 5432, cast=int)}',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env("TIME_ZONE", "Africa/Douala")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app_models.User'

# SUPER_USER
SUPER_FIRST_NAME = env("SUPER_FIRST_NAME", "Super")
SUPER_LAST_NAME = env("SUPER_LAST_NAME", "Admin")
SUPER_USER_EMAIL = env("SUPER_USER_EMAIL", "super_admin@email.com")
SUPER_USER_PHONE = env("SUPER_USER_PHONE", "699999999")
SUPER_USER_PASSWORD = env("SUPER_USER_PASSWORD", "password")

# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

# JWT AUTH SETTINGS
TOKEN_VALIDITY = env("TOKEN_VALIDITY", 60 * 24, cast=int)   # 1 day = 24 hours
JWT_AUTH = {
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_EXPIRATION_DELTA": datetime.timedelta(minutes=TOKEN_VALIDITY),
    "JWT_ALLOW_REFRESH": True,
}

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}
