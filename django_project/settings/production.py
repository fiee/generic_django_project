#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PROJECT_NAME,                      # Or path to database file if using sqlite3.
        'USER': PROJECT_NAME,                      # Not used with sqlite3.
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUESTS': True,                  # Wrap everything in transactions.
    }
}
