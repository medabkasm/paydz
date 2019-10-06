"""
Django settings for paysera project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.contrib.messages import constants as messages
from	django.utils.translation	import	gettext_lazy	as	_
import json
import django_heroku


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



with open("env_variables.js") as envVars:
    vars = json.loads(envVars.read())[0]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'y6!-x=mp-2c(uiw(37*x!#%%1s7t7f8p_k4cfbiy1$g59^)bux'
#SECRET_KEY = 'y6!-x=mp-2c(uiw(37*x!#%%1s7t7f8p_k4cfbiy1$g59^)bux'
SECRET_KEY = vars['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['192.168.43.246','127.0.0.1','localhost']
ALLOWED_HOSTS = ['192.168.43.246', '127.0.0.1', 'localhost','6b6ee814.ngrok.io','paydz.herokuapp.com']
PASSWORD_RESET_TIMEOUT_DAYS = 1

# Application definition

INSTALLED_APPS = [

    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'home',
    'accounts',
    'offers',
    'notifications',
    'profiles',



]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]



ROOT_URLCONF = 'paysera.urls'
ASGI_APPLICATION = "paysera.routing.application"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'paysera/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication

    'django.contrib.auth.backends.ModelBackend',
)



WSGI_APPLICATION = 'paysera.wsgi.application'


CHANNEL_LAYERS = {
    "default" : {
        "BACKEND" : 'channels_redis.core.RedisChannelLayer',
        "CONFIG" : {
            "hosts" : [ ('127.0.0.1',6379)],
        },
    },
}




# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'USER': ''  ,    # not required for sqllite.
        #'PASSWORD': ''  , # not required for sqllite.
        #'HOST': '' , # empty for local host , not required for sqllite.
        #'PORT': ''  # empty for local host , not required for sqllite.
    }
}




# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/


AUTH_USER_MODEL = 'accounts.User'


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}



LANGUAGE_CODE = 'en-us'

LANGUAGES = (
('en', _('English')),
('ar',_('Arab')),
('fr',_('Frensh')),
    )


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR,'mediafiles')
MEDIA_URL = '/accounts/media/user_photos/'
LOCALE_PATHS = (
    os.path.join(BASE_DIR,'locale/'),
)

LOGIN_URL = 'accounts:login'
LOGOUT_URL ='accounts:login'
LOGIN_REDIRECT_URL = 'home:posts'




# email configurations.

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = vars['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = vars['EMAIL_HOST_PASSWORD']


'''
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
'''

# recaptcha configurations.
CAPTCHA_SITE = vars['CAPTCHA_SITE2']
GOOGLE_RECAPTCHA_SECRET_KEY = vars['GOOGLE_RECAPTCHA_SECRET_KEY2']

# social django configurations.
SOCIAL_AUTH_PIPELINE = (

    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',

)
SOCIAL_AUTH_USER_MODEL = 'accounts.User'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['name', 'email']









    # google+
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = vars['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = vars['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']



    # facebook
SOCIAL_AUTH_FACEBOOK_KEY = vars['SOCIAL_AUTH_FACEBOOK_KEY2']
SOCIAL_AUTH_FACEBOOK_SECRET = vars['SOCIAL_AUTH_FACEBOOK_SECRET2']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
      'fields': 'id ,name'
    }
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
        ('name', 'name'),
        ('email', 'email'),
    ]


# social authantication configurations.
SOCIAL_AUTH_LOGIN_ERROR_URL = 'home:posts'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'home:posts'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
#static file directory inclusion
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'paysera/static') ,]

# Activate Django-Heroku.
django_heroku.settings(locals())
