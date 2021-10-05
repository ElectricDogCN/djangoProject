"""
ASGI config for djangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import threading

from django.core.asgi import get_asgi_application

from djangoProject.websocket import websocket_application

from djangoProject import socket as ss

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

django_application = get_asgi_application()

s_server = ss.SocketServer()
s_server.accept_thread()



async def application(scope, receive, send):
    if scope['type'] == 'http' or scope['type'] == 'https':
        await django_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
