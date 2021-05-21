from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['humansof42.com', 'www.humansof42.com', '34.64.112.133', ]

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
