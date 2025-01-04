import platform

# noinspection PyUnresolvedReferences
from .base import *

# Security

DEBUG = True

SECRET_KEY = '5cw1)q4ww+ckr5wevw@wr2zymp57$k@4fy3*@h2%(l79bx5b9i'

ALLOWED_HOSTS = []

PUBLIC_URL = 'http://localhost:8000'

INTERNAL_IPS = [
    '127.0.0.1'
]


# Application

INSTALLED_APPS = [
    # Used for WebSockets without Gunicorn/Uvicorn
    'daphne',
] + INSTALLED_APPS + [
    'debug_toolbar',

    # Only used to generate database diagrams, i.e. do not use other features of this package
    'django_extensions'
]


# Middleware

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

# Cross-Origin Resource Sharing (CORS)

CORS_ALLOWED_ORIGINS = []


# Cross Site Request Forgery (CSRF)

CSRF_TRUSTED_ORIGINS = []


# Authentication

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'


# Email

EMAIL_BACKEND = 'pandora.core.email.EmailBackend'
EMAIL_FILE_PATH = '/tmp/pandora-emails'


# Channels

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

if platform.system() == 'Darwin':
    GDAL_LIBRARY_PATH = "/opt/homebrew/lib/libgdal.dylib"
    GEOS_LIBRARY_PATH = "/opt/homebrew/lib/libgeos_c.dylib"
