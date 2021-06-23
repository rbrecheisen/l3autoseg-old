import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = '{}/data/l3autoseg'.format(os.environ['HOME'])

SECRET_KEY = os.environ.get('SECRET_KEY', '1234')

DEBUG = True if os.environ.get('DEBUG', 1) == 1 else False

SQLITE3_DIR = os.environ.get('SQLITE3_DIR', ROOT_DIR)

# This directory should already exist and contain TensorFlow model files
TENSORFLOW_MODEL_DIR = '/mnt/localscratch/maastro/Leroy/bodycomposition/logs/gradient_tape/stability_new_params_contour/20210529-084544/saved_models/model_26200'
TENSORFLOW_PARAMS_FILE = '/mnt/localscratch/maastro/Leroy/bodycomposition/logs/gradient_tape/stability_new_params_contour/20210529-084544/params.json'

ALLOWED_HOSTS = [
    '137.120.191.233',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rq',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SQLITE3_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6378,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
os.makedirs(STATIC_ROOT, exist_ok=True)

MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'files')
os.makedirs(MEDIA_ROOT, exist_ok=True)
