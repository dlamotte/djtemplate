#!/usr/bin/env python
import os
import sys
from os import path

if __name__ == '__main__':
    root = path.dirname(path.abspath(__file__))
    if path.exists(path.join(root, 'settings_local.py')):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_local')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
    sys.path.insert(0, root)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
