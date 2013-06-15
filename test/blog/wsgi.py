#!/usr/bin/env python

import os

APPLICATION = os.environ.get('DJANGO_APPLICATION_NAME')

os.environ.setdefault(
  'DJANGO_SETTINGS_MODULE', '%s.settings' % APPLICATION
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
