import os

from django.core.wsgi import get_wsgi_application

from application.sentry import initialize_sentry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.production')

application = get_wsgi_application()

initialize_sentry()
