# -- coding: utf-8 --
"""
Django settings for sistema project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_6(9kra#gn_78rrkiowvh3!^d60m+w(kh16#=5*!lkpcunoh@)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'backup',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'actividades',
    'alumnos',
    'clases',
    'inicio',
    'horarios',
    'instrumentos',
    'profesores',
    'reportes',
)

MYSQLDUMP = '/usr/bin/mysqldump'
GRAPPELLI_ADMIN_TITLE = 'Sistema de Registro y Control de Alumnos del Núcleo Quíbor'

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_URL = reverse_lazy('logout')


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Finaliza la sesion en X cantidad de segundos
# SESSION_COOKIE_AGE = 6

# Finaliza la sesion al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'sistema.urls'

WSGI_APPLICATION = 'sistema.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'orquesta',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_general_ci' },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

# USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "django.core.context_processors.request",
)