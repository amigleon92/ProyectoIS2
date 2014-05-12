"""
Django settings for ProyectoIS2 project.

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
SECRET_KEY = 'u9lvrfu5f8^k0zy5y9*$)!_#b9#@*y^@kuu4b72^4t0drw8ulf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Aplicaciones.Fase',
    'Aplicaciones.Login',
    'Aplicaciones.Proyecto',
    'Aplicaciones.Rol',
    'Aplicaciones.Usuario',
    'Aplicaciones.Item',
    'Aplicaciones.Tipo_de_Item',
    'Aplicaciones.Tipo_de_Atributo',
    'Aplicaciones.Atributo',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ProyectoIS2.urls'

WSGI_APPLICATION = 'ProyectoIS2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'GrupoR05_IS2',
        'HOST':'localhost',
        'USER': 'R05_is2',
        'PASSWORD': 'R05_is2'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-py'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

from unipath import Path

RUTA_PROYECTO= Path(__file__).ancestor(2)

TEMPLATE_DIRS= (
    RUTA_PROYECTO.child('templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS= (
    RUTA_PROYECTO.child('static'),
)

STATIC_URL = '/static/'
