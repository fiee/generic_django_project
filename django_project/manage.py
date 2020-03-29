#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import dotenv
import logging
logging.captureWarnings(True)  # dotenv uses warnings

current_dir = os.path.dirname(__file__)
# try to load .env file from current directory (I use that in development);
# if that fails (you’ll get a harmless warning), try the project’s base path.
if not dotenv.read_dotenv(os.path.join(current_dir, '.env')):
    dotenv.read_dotenv(os.path.abspath(os.path.join(current_dir, '../../..', '.env'))) # '/var/www/project_name/.env'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
