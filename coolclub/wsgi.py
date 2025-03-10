"""
WSGI config for coolclub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolclub.settings")
print("Starting WSGI application")
application = get_wsgi_application()
print("WSGI application loaded successfully")
