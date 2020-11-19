from __future__ import unicode_literals

import os

INSTALLED_APPS = [
    'wagtail_annotations',
    'tests.app',

    'taggit',
    'modelcluster',

    'wagtail.core',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.users',
    'wagtail.sites',
    'wagtail.snippets',
    'wagtail.images',

    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
]

SECRET_KEY = 'not a secret'

ROOT_URLCONF = 'tests.app.urls'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

WAGTAIL_SITE_NAME = 'Wagtail Annotated Images'

DEBUG = True

USE_TZ = True
TIME_ZONE = 'Australia/Hobart'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_URL = '/media/'
