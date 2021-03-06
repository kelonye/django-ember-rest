#!/usr/bin/env python

import os
import sys

if __name__ == '__main__':

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    APPLICATION = 'server'

    os.environ.setdefault(
      'DJANGO_APPLICATION_NAME', APPLICATION
    )
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', '%s.settings' % APPLICATION
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
