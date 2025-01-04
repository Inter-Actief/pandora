import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from application.sentry import initialize_sentry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.production')

# Initialize Django before importing application code
get_asgi_application()

from pandora.websocket_urls import urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    'http': get_asgi_application(),

    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(urlpatterns)
        )
    )
})

initialize_sentry()
