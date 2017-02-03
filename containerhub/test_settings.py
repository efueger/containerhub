# coding: utf-8

from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

HOST_IP = '127.0.0.1'