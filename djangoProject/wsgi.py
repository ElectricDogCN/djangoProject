"""
WSGI config for djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from djangoProject import socket as ss

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
ss.s_server.accept_thread()


application = get_wsgi_application()
