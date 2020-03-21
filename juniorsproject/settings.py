"""
Django settings for juniorsproject project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url
from django.conf import settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '#p-lw@xy(im8)96s_j-tj&1gy)_7&n$b6^2@kt1m%u0#6158i%'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '#p-lw@xy(im8)96s_j-tj&1gy)_7&n$b6^2@kt1m%u0#6158i%')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



ALLOWED_HOSTS = ['juniors-app.herokuapp.com','127.0.0.1', '0.0.0.0']


# Application definition

INSTALLED_APPS = [

    # users app 
    'users',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # our apps 
    'reports',
    'groups',
    'posts',
    'notifications',
    'comments',
    'messenger',
    'esearch',

    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # crispy 
    'crispy_forms',
    
    # django contries 
    'django_countries',

    # bootstrap-datepicker 
    'bootstrap_datepicker_plus',
    'bootstrap4',


    # allauth outh website
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',

    'rest_framework',
    'emoticons',

    # Django toolbar 
    'debug_toolbar',


]

SITE_ID = 2



AUTHENTICATION_BACKENDS = (
    # Default backend -- used to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'juniorsproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'groups.context_processors.SubscriptionList',

            ],
        },
    },
]

WSGI_APPLICATION = 'juniorsproject.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'juniors',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'


CRISPY_TEMPLATE_PACK = 'bootstrap4'
AUTH_PROFILE_MODULE = 'users.CustomUser'

AUTH_USER_MODEL = 'users.CustomUser' 

LOGIN_URL = 'posts:home'
LOGOUT_REDIRECT_URL = 'posts:home'
LOGIN_REDIRECT_URL = 'posts:home'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_QUERY_EMAIL = True

# SESSION_COOKIE_AGE = 400

handler404 = 'juniorsproject.views.error_404'
handler500 = 'juniorsproject.views.error_500'
handler403 = 'juniorsproject.views.error_403'
handler400 = 'juniorsproject.views.error_400'

# DEBUG = False


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
