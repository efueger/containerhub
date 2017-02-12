from .settings import *

SECRET_KEY = 'test_naew6iequ5Thuzooche1uquooghoobaesoaNgeiyunoe6Iquuwahng3bie1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

HOST_IP = '127.0.0.1'