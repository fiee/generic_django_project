#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # get out of settings
PROJECT_NAME = os.path.split(PROJECT_ROOT)[-1]
rootrel = lambda p: os.path.abspath(os.path.join(PROJECT_ROOT, p))

bind = 'unix:/var/run/django.socket'
# bind = '127.0.0.1:8'+str(os.getuid())[1:]
workers = 1
#worker_class = 'eventlet'
#max_requests = 2048
pidfile = '/var/run/django.pid'
user = 'project_name' # adapt!
group = 'staff' # adapt
logfile = rootrel('logs/gunicorn.log')
#loglevel = 'info'
proc_name = 'gunicorn-'+PROJECT_NAME
