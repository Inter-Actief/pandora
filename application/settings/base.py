import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv


def parse_boolean(value: str):
    try:
        return value.lower() in ['true', '1'] if value is not None else False
    except ValueError:
        return False


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Security

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = parse_boolean(os.getenv('DEBUG'))

ALLOWED_HOSTS = [origin.strip() for origin in os.getenv('ALLOWED_HOSTS', '').split(',')]

PUBLIC_URL = os.getenv('PUBLIC_URL')


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_bootstrap5',
    'django_filters',
    'import_export',
    'qr_code',
    'pandora.core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'pandora.editions',
    'pandora.pregames',
    'pandora.puzzles',
    'pandora.teams',
    'pandora.themes'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    'django_request_cache.middleware.RequestCacheMiddleware',
]

ROOT_URLCONF = 'pandora.urls'


def context_variables(_request):
    from django.conf import settings
    return {
        'PUBLIC_URL': settings.PUBLIC_URL
    }


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'application.settings.base.context_variables',
            ]
        },
    },
]

ASGI_APPLICATION = 'application.asgi.application'
WSGI_APPLICATION = 'application.wsgi.application'

SITE_ID = 1


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'USER': os.getenv('DATABASE_USERNAME', 'pandora'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'NAME': os.getenv('DATABASE_NAME', 'pandora'),
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'


# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL
    },
    'qr-code': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'KEY_PREFIX': 'qr_code_',
        'TIMEOUT': 7 * 24 * 60 * 60
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en'

TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Amsterdam')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English')
]


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'dist', 'static')
STATICFILES_DIRS = []


# Media files (user uploads)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'dist', 'media'))


# Cross-Origin Resource Sharing (CORS)

CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')]

CORS_ALLOW_CREDENTIALS = False


# Cross Site Request Forgery (CSRF)

CSRF_COOKIE_DOMAIN = os.getenv('CSRF_COOKIE_DOMAIN')

CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')]


# Session

SESSION_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = True


# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USE_TLS = parse_boolean(os.getenv('EMAIL_USE_TLS', 'true'))

DEFAULT_FROM_EMAIL = os.getenv('EMAIL_FROM', EMAIL_HOST_USER)


# Authentication

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

# TODO: remove hardcoded year
LOGIN_REDIRECT_URL = reverse_lazy('dashboard', kwargs={'year': 2024})
LOGOUT_REDIRECT_URL = reverse_lazy('home')

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USER_DISPLAY = 'application.settings.base.get_user_display_name'
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_FORMS = {
    'login': 'pandora.core.forms.LoginForm',
    'signup': 'pandora.core.forms.SignupForm'
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True
    },
    'microsoft': {
        'OAUTH_PKCE_ENABLED': True
    }
}


def get_user_display_name(user):
    return user.email


# Sentry

SENTRY_DSN = os.getenv('SENTRY_DSN')
SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT')


# Channels

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST', 'localhost'), 6379)]
        }
    }
}


# QR Codes

QR_CODE_CACHE_ALIAS = 'qr-code'
