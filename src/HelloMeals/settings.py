"""
Django settings for HelloMeals project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r#se5okdi6e$n9oae3jl8)%%erl#-q4wymb0@9@r5_14&0v$02'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

MEDIA_ROOT = BASE_DIR / 'data' / 'media'

MEDIA_URL = '/media/'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    # 'http://localhost:6733',
    # 'http://127.0.0.1:6733',
    os.getenv('APP_URL') if os.getenv('APP_URL') else 'http://127.0.0.1:6733',
]
CORS_ALLOW_ALL_ORIGINS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',
    'rql_filter',
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'widget_tweaks',
    'pwa',
    'django_cleanup.apps.CleanupConfig',
    'dynamic_preferences',
    'dynamic_preferences.users.apps.UserPreferencesConfig',

    'Apps.MealManager',
    'Apps.ClientManager',
    'HelloMeals',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['dj_rql.drf.RQLFilterBackend', 'django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=56),
}

ROOT_URLCONF = 'HelloMeals.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "Apps" / "ClientManager" / "templates" / "ClientManager" / "pages"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamic_preferences.processors.global_preferences',
            ],
        },
    },
]

WSGI_APPLICATION = 'HelloMeals.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hellomeals',
        'USER': os.getenv("POSTGRES_USER", "root"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "root"),
        'HOST': os.getenv("POSTGRES_HOST", "127.0.0.1"),
        'PORT': "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [('en', 'English'), ('de', 'Deutsch')]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'Apps/ClientManager', 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "{levelname} {asctime}: {module} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            'class': 'logging.handlers.RotatingFileHandler',
            "filename": BASE_DIR / 'data' / 'log.log',
            'maxBytes': 500000,
            'backupCount': 2,
            "formatter": "basic",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        'django.utils.autoreload': {
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db': {
            'level': 'WARNING',
            'propagate': False,
        },
        'urllib3': {
            'handlers': [],
            'level': 'WARNING',
            'propagate': False,
        },
        'http.server': {
            'handlers': [],
            'level': 'WARNING',
            'propagate': False,
        },
        "http.client": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "Basehttp": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "PIL.TiffImagePlugin": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    }
}

PWA_APP_NAME = 'HelloMeals'
PWA_APP_DESCRIPTION = "Selfhosted HelloFresh recipe manager"
PWA_APP_THEME_COLOR = '#0F172A'
PWA_APP_BACKGROUND_COLOR = '#0F172A'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/Home'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/logo/512px.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/logo/512px.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
