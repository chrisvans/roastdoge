from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'roastdog',
        'USER': 'chris',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}