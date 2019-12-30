#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import dotenv
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.get_env_variable('DJANGO_SETTINGS_MODULE'))
current_dir = os.path.dirname(__file__)
try:
    dotenv.read_dotenv(os.path.join(current_dir, '.env'))
except UserWarning:
    dotenv.read_dotenv(os.path.abspath(os.path.join(current_dir, '../../..', '.env')))

app = Celery('cerebrale')


# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
