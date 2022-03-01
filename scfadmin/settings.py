from pathlib import Path
import os
import dj_database_url
import dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# env config
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# IMPORTANT CONFIG'S
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

# ALLOWED_HOSTS = ['tfxworld.com','*','*.tfxworld.com','.tfxworld.com','icici.tfxworld.com','142.93.218.145']

ALLOWED_HOSTS = ['tfxworld.com', '*', '*.tfxworld.com', '.tfxworld.com']

INTERNAL_IPS = [
    "127.0.0.1",
]




# COMMENT THIS BEFORE USING TENANT'S

INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'transaction',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_swagger',
    'graphene_django',
    'debug_toolbar',
    'silk.apps.SilkAppConfig'
]


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# TENANT CONFIGURATIONS
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# SHARED_APPS = [
#     'django_tenants',
#     'client',
#     # 'jazzmin',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'accounts',
#     'rest_framework',
#     'rest_framework.authtoken',
#     'corsheaders',
#     'rest_framework_swagger',

# ]


# TENANT_APPS = [
#     # 'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'transaction',
#     'rest_framework',
#     'rest_framework.authtoken',
#     'rest_framework_swagger',
#     'graphene_django',
# ]

# INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]


# TENANT_MODEL = "client.Client"

# TENANT_DOMAIN_MODEL = "client.Domain"

# PUBLIC_SCHEMA_URLCONF = 'scfadmin.urls_public'

# SHOW_PUBLIC_IF_NO_TENANT_FOUND = True


# DATABASE_ROUTERS = (
#     'django_tenants.routers.TenantSyncRouter',
# )


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# END OF TENANT CONFIGURATIONS
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    # 'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'silk.middleware.SilkyMiddleware',
]



# WHITENOISE  AND CORS SETTINGS


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'scfadmin.urls'



# DEFAULT TEMPLATES AND 404

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

WSGI_APPLICATION = 'scfadmin.wsgi.application'


# –––––––––––––––––––––––––––––––––––––––––#
#             DATABASE SETUP               #
# –––––––––––––––––––––––––––––––––––––––––#


# DATABASES = {}

# DATABASES['default'] = dj_database_url.config(conn_max_age=600)



# # DATABASE HEROKU ADD - ON

# DATABASES = {
#     'default': {
#         'ENGINE': 'django_tenants.postgresql_backend',
#         'NAME': 'd528p0is7igtu6',
#         'USER': 'ldnnbocejvuzoo',
#         'PASSWORD': '4698bf5b5d65efe1a546101bec7f2e57a359ad4f9522ab9b8987154da915cca7',
#         'HOST': 'ec2-52-3-130-181.compute-1.amazonaws.com',
#         'PORT': '5432',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'scf2',
        'USER': 'sheik',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}





# TESTING SQLITE

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# CUSTOM AUTH BACKEND

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backend.AuthenticationBackend',
]


# EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_ID']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_APP_PASSWORD']



# REST FRAMEWORK AUTH TOKEN AND SETTINGS

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated",
    'rest_framework.permissions.AllowAny'],

    # "DATE_INPUT_FORMATS": ["%d-%m-%Y"]
}


# CACHE FOR SCF

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#         'LOCATION': '127.0.0.1:8000',
#     }
# }