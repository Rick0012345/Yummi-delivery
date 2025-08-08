from .base import *
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(os.path.join(BASE_DIR, 'dotenv', '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1')

# Configurar hosts para desenvolvimento/produção
ALLOWED_HOSTS = ['*']  # Simplificado para desenvolvimento

# Configurar CSRF para desenvolvimento/produção
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://yummi-delivery-production.up.railway.app',
]

# Configurar CORS para desenvolvimento/produção
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://yummi-delivery-production.up.railway.app',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Simplificado para desenvolvimento

# Database para produção (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('PASSWORD_RAILWAY'),
        'HOST': os.getenv('HOST_RAILWAY'),
        'PORT': os.getenv('PORT_RAILWAY'),
    }
}

# Configurações de arquivos estáticos para produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging para produção
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
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

# Configurações simplificadas para desenvolvimento/teste

# Email backend simplificado (console para desenvolvimento)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache simplificado (local memory)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Configurações de sessão simplificadas para desenvolvimento
SESSION_COOKIE_SECURE = False  # Permite HTTP para desenvolvimento
CSRF_COOKIE_SECURE = False     # Permite HTTP para desenvolvimento
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Configurações de arquivos estáticos
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]