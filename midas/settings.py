

from pathlib import Path
# configure environment for deployment
import dj_database_url
import environ
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'. old
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()

environ.Env.read_env()

# Take environment variables from .env file
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING:
# SECRET_KEY = 'django-insecure-p=tt6(je38hm4$2k5wt1xecbzvuzqfmqyv%4o8486t9^90k26n'

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# dev
# DEBUG = True

# for production
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['midasapiv1-production.up.railway.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # config
    'djoser',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    
    # apps
    'users',
    'core',
    'profiles',
    'cooperators',
    'drf_spectacular',
 ]

# WORKED
# ALLOWED_HOSTS=['*']

# CORS_ORIGIN_ALLOW_ALL = True


# ALLOWED_HOSTS=['http://localhost:8080','http://localhost:8000']

               
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://midastouchonline.co',
    'https://www.midastouchonline.co',
    'https://midas-frontend.onrender.com',
    # 'localhost:8080',
    # 'localhost:8081',
)

# config
# CORS_ALLOWED_ORIGIN=[
#     'http://localhost:8080',
#     # 'http://127.0.0.1:8080',
# ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'midas.urls'

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

WSGI_APPLICATION = 'midas.wsgi.application'




# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         # 'NAME':'midas_api',
#         # 'USER': 'postgres',
#         # 'PASSWORD':'2021_lonax',
        
#         'NAME':'midas_production_db',
#         'USER': 'postgres',
#         'PASSWORD':'2021_lonax',
#         'HOST':'localhost',
#     }
# }

# production

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':'railway',
#         'USER': 'postgres',
#         'PASSWORD':'IATtrypy9yzd2ITLRCQ5',
#         'HOST':'containers-us-west-18.railway.app',
#         'PORT':'5435',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':env('NAME'),
        'USER':env('USER'),
        'PASSWORD':env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT':env('PORT'),
    }
}

# DATABASES={
#     'default': dj_database_url.parse(env('DATABASE_URL'))
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'MIDAS Project API',
    'DESCRIPTION': 'An app to manage records of a small cooperative society',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# custom user
AUTH_USER_MODEL = 'users.CustomUser'