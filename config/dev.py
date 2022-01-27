"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.13.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["H42_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

WHITENOISE_AUTOREFRESH = True

# mail setting
ADMINS = [('Yeji Choi', 'saluthuge@gmail.com'), ('humansof42','humansof42@gmail.com')]

MANAGERS = ADMINS

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'humansof42@gmail.com'

EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'humansof42@gmail.com'


#log setting

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
	    'filename': os.path.join(BASE_DIR, 'debug.log'),
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins',],
            'level': 'ERROR',
	        'propagate': True,
        },
    }
}

ALLOWED_HOSTS = ['*', 'localhost', 'humansof42.com', 'www.humansof42.com', '34.64.112.133', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'interview',
    'user',
    'rest_framework',
    'django_summernote',
    'imagekit',
    'sorl.thumbnail',
    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'h42',
        'USER': 'yechoi',
	    'PASSWORD': 'bonjour12',
	    'HOST': 'localhost',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
	STATIC_DIR,
]
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Summernote

SUMMERNOTE_CONFIG = {
    'attachment_filesize_limit': 10 * 1024 * 1024
}

# File upload size adjust
#
DATA_UPLOAD_MAX_MEMORY_SIZE = None
#
# FILE_UPLOAD_MAX_MEMORY_SIZE = None

SECRET_INTO_FILE = os.path.join(BASE_DIR, 'config', 'secret_into_file.json')

with open(SECRET_INTO_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f"Set the {setting} environment variable"
        raise ImproperlyConfigured(error_msg)


FT_UID_KEY = os.environ.get('FT_UID_KEY', get_secret("FT_UID_KEY"))
FT_SECRET_KEY = os.environ.get('FT_SECRET_KEY', get_secret("FT_SECRET_KEY"))
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', get_secret("EMAIL_HOST_PASSWORD"))

AUTH_USER_MODEL = 'user.User'

LOGIN_URL = '/login/'

