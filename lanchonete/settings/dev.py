from .base import *
import os
from pathlib import Path

# Carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / 'dotenv' / '.env'
    load_dotenv(env_path)
    print(f"Variáveis de ambiente carregadas de {env_path}")
except ImportError:
    print("python-dotenv não está instalado. As variáveis de ambiente não serão carregadas do arquivo .env.")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1')

# Configurar hosts para desenvolvimento
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# Configurar CSRF para desenvolvimento
CSRF_TRUSTED_ORIGINS = os.getenv('DJANGO_CSRF_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')

# Configurar CORS para desenvolvimento
CORS_ALLOWED_ORIGINS = os.getenv('DJANGO_CORS_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')
CORS_ALLOW_CREDENTIALS = True

# Database para desenvolvimento (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'lanchonete_dev'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres123'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
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