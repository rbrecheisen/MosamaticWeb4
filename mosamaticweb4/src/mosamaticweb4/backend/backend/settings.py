import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR_LOCAL = os.path.join(Path.home(), 'MosamaticWeb4/data')
DATA_DIR = os.environ.get('DATA_DIR', DATA_DIR_LOCAL)
MODELS_DIR = os.path.join(Path.home(), 'MosamaticWeb4/models')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

SECRET_KEY = 'django-insecure-05lf8*j1e@nfcc^!94rrjg)m0l#$@a=93*g*8y+@twaoc68#nd'

DEBUG = True

ALLOWED_HOSTS = []

ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'session_security',
    'crispy_forms',
    'crispy_bootstrap5',
    'app',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'mosamaticweb4': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SESSION_SECURITY_WARN_AFTER = 840
SESSION_SECURITY_EXPIRE_AFTER = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MEDIA_URL = '/filesets/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'filesets')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'