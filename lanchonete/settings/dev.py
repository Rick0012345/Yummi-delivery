from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1')

# Configurar hosts para desenvolvimento
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# Configurar CSRF para desenvolvimento
CSRF_TRUSTED_ORIGINS = os.environ.get('DJANGO_CSRF_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')

# Configurar CORS para desenvolvimento
CORS_ALLOWED_ORIGINS = os.environ.get('DJANGO_CORS_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')
CORS_ALLOW_CREDENTIALS = True

# Database para desenvolvimento (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configurações de arquivos estáticos para desenvolvimento
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging para desenvolvimento
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configurações de email para desenvolvimento (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações de cache para desenvolvimento
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Configurações de sessão para desenvolvimento
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Configurações de segurança para desenvolvimento
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False 