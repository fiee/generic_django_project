#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
# import os
from .base import *

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# PROJECT_NAME = os.path.split(PROJECT_ROOT)[-1]


def rootrel(p):
    # print "local rootrel %s" % p
    return os.path.abspath(os.path.join(PROJECT_ROOT, p))

DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': rel('dev_db.sqlite3'),          # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),                  # Not used with sqlite3.
        'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUESTS': True,                  # Wrap everything in transactions.
    }
}

FEINCMS_THUMBNAIL_DIR = 'medialibrary/_thumbs/'
MEDIA_ROOT = rel('media')
MEDIALIBRARY_ROOT = rel('media') #/medialibrary')

if DEBUG:
    # INSTALLED_APPS.append('django.contrib.admindocs')
    # INSTALLED_APPS.append('debug_toolbar')
    # MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')  # see also http://github.com/robhudson/django-debug-toolbar/blob/master/README.rst
    LOGGING['handlers']['file'] = {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': rootrel('logs/info.log'),
            }
    LOGGING['handlers']['error_file'] = {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': rootrel('logs/error.log'),
            }

SECURE_SSL_REDIRECT = False  # if all non-SSL requests should be permanently redirected to SSL.
SESSION_COOKIE_SECURE = False  # if you are using django.contrib.sessions (True blocks admin login)

import warnings
warnings.filterwarnings(
        'error', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')
