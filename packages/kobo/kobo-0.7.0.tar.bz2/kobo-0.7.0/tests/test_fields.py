#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.environ["PYTHONPATH"] = PROJECT_DIR
os.environ['DJANGO_SETTINGS_MODULE'] = 'fields_test.settings'
sys.path.insert(0, PROJECT_DIR)

from django.core.management import call_command
import django

# Django >= 1.7 must call this method to initialize app registry,
# while older Django do not have this method
if 'setup' in dir(django):
    django.setup()

call_command('test', 'fields_test')
#call_command('syncdb')
