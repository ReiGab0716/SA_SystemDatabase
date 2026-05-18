"""
Django settings for core project.
"""

from pathlib import Path
import os

import dj_database_url
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'jazzmin',           # MUST be at the very top to override default admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clinic',            # Your project app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Must be above Messages
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'clinic.middleware.NoStoreAuthenticatedMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', # Must be below Sessions & Auth
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'clinic.context_processors.staff_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# Use DATABASE_URL in production. Local development can continue using the
# PostgreSQL values from .env.
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='shields_aesthetics_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='127.0.0.1'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = config('TIME_ZONE', default='Asia/Manila')
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = Path(config('MEDIA_ROOT', default=str(BASE_DIR / 'media')))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        # Jazzmin ships a Bootstrap source-map reference without the map file,
        # so use compressed static storage instead of manifest hashing.
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# Production security settings. Keep DEBUG=True in .env for local development.
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0 if DEBUG else 31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=not DEBUG, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=not DEBUG, cast=bool)

# --- JAZZMIN SETTINGS ---

JAZZMIN_SETTINGS = {
    "site_title": "Shields Aesthetics Admin",
    "site_header": "Shields Aesthetics",
    "site_brand": "Shields Aesthetics",
    
    # 1. THE TAB ICON
    # Keeping this ensures the phoenix stays on your browser tab
    "site_logo": "images/shield_logo.png",  

    # 2. THE NUCLEAR REMOVAL
    # By using "none" as a string (not None), Jazzmin attempts to find 
    # a file named 'none', fails, and displays nothing on the login page.
    "login_logo": "none", 
    "login_logo_dark": "none",
    
    "site_logo_classes": "img-circle", 
    "welcome_sign": "Welcome to Shields Aesthetics Management System",
    "copyright": "Shields Aesthetics Ltd",
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False, 
}

JAZZMIN_UI_TWEAKS = {
    "navbar_theme": "navbar-white",
    "navbar": "navbar-light",
    "theme": "simplex",
    "sidebar": "sidebar-light-primary",
    "accent": "accent-primary",
    "navbar_fixed": True,
}

# AUTHENTICATION REDIRECTS
LOGIN_REDIRECT_URL = 'login_redirect'
LOGIN_URL = 'login'
