#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import dotenv
import logging
logging.captureWarnings(True)  # dotenv uses warnings

current_dir = os.path.abspath(os.path.dirname(__file__))
# try to load .env file from current directory or look upwards
while current_dir and not os.path.isfile(os.path.join(current_dir, '.env')):
    current_dir = "/".join(os.path.split(current_dir)[:-1])

env = os.path.join(current_dir, '.env')
if not os.path.isfile(env):
    print("Configuration environment file (.env) not found!")
    sys.exit(1)
dotenv.read_dotenv(env)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
