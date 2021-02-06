import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pops_website.settings")
django.setup()

from channels.auth import AuthMiddlewareStack

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": AsgiHandler(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)
