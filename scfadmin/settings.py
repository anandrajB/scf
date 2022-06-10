from pathlib import Path
import os
import dotenv


# –––––––––––––––––––––--#
#  IMPORTANT CONFIG - 1  #
# –––––––––––––––––––––--#

BASE_DIR = Path(__file__).resolve().parent.parent


dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# –––––––––––––––––––––-#
#  IMPORTANT CONFIG - 2 #
# ––––––––––––––––––––-–#

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = os.environ['SECRET_KEY']

AUTH_USER_MODEL = 'accounts.User'


# APPEND_SLASH=False



# –––––––––––––––––––––#
#  HIGH PRIORITY - 1   #
# –––––––––––––––––––––#

DEBUG = True

# if production false , the project uses heroku db
PRODUCTION = False

# ALLOWED_HOSTS = ['tfxworld.com','*','*.tfxworld.com','.tfxworld.com','icici.tfxworld.com','142.93.218.145']

ALLOWED_HOSTS = ['*']



# FOR DEBUG LOCAL
INTERNAL_IPS = [
    "127.0.0.1",
]



# COMMENT THIS BEFORE USING TENANT'S

INSTALLED_APPS = [
    'jazzmin',
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
]



# –––––––––––––––––––––#
#  TENANT CONFIG'S     #   # un-comment below section when using tenant's
# –––––––––––––––––––––#



# SHARED_APPS = [
#     'django_tenants',
#     'client',
#     'jazzmin',
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
#     'accounts',
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


# –––––––––––––––––––––––––––––––#
#  END OF TENANT CONFIGURATIONS  #
# –––––––––––––––––––––––––––––––#





# ––––––––––---#
#  MIDDLEWARE  #
# –––––––––----#

# Middleware ! uncomment the first line when using tenant 

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
]


# –––––––––––––––––––---------––#
#  WHITE NOISE AND CORS SETTING #
# –––––––––––––––––––---------––#


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'scfadmin.urls'


# –––––––––––––––––––––#
#  TEMPLATED FOR HTML  #
# –––––––––––––––––––––#

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
                'django.template.context_processors.media',
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


# DATABASE HEROKU  heroku testing database


# –––––––––––––––––––––#
#  HIGH PRIORITY - 2   #
# –––––––––––––––––––––#


# SETUP : 1

if PRODUCTION :
    # digital ocean droplet database 
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': 'scf',
            'USER': 'anand',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    
else:
    # heroku test environment database
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': 'da0oesk9k524m6',
            'USER': 'bneyoefyrsqnbt',
            'PASSWORD': 'e9b31e4f2a78949ef2a1117725ddd54a7269283e696dc7c6224e3c44316a2ca7',
            'HOST': 'ec2-52-54-212-232.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }




# SETUP : 2 ( localhost )

# DATABASES = {
#     'default': {
#         'ENGINE': 'django_tenants.postgresql_backend',
#         'NAME': 'scf11',
#         'USER': 'postgres',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }



# –––––––––––––––––––––#
#  DEFAULT VALIDATORS  #
# –––––––––––––––––––––#


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



# –––––––––––––––––––––#
# INTERNATIONALIZATION #
# –––––––––––––––––––––#

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# –––––––––––––––––––––#
#     STATIC FILES     #
# –––––––––––––––––––––#


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


# media related fiels for invoice upload
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# MEDIA_URL = "http://127.0.0.1:8000/media/"

MEDIA_URL = '/media/'

# –––––––––––––––––––––#
#     AUTH BACKEND     #
# –––––––––––––––––––––#

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backend.AuthenticationBackend',
]


# –––––––––––––––––––#
#  EMAIL  CONFIG'S   #
# –––––––––––––––––––#


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_ID']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_APP_PASSWORD']


# –––––––––––––––––––––----#
#  TOKEN AND REST SETTING  #
# –––––––––––––––––––––----#

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
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 'EXCEPTION_HANDLER': 'accounts.exception_handler.custom_exception_handler'
}



# ––––––––––––––––-----–––––#
#   REDIS CACHE'S CONFIG    #
# –––––––––––––-----––––––––#

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# –––––––––––––––––––––#
#    GRAPH QL CONFIG   #
# –––––––––––––––––––––#

GRAPH_MODEL = {
    "all_applications":True,
    "group_models":True,
}






# ––––––––––––––------–––––––#
#    SSL TLS CONFIGURATION   #
# ––––––––––––––––------–––––#

# CORS_REPLACE_HTTPS_REFERER      = False
# HOST_SCHEME                     = "http://"
# SECURE_PROXY_SSL_HEADER         = None
# SECURE_SSL_REDIRECT             = False
# SESSION_COOKIE_SECURE           = False
# CSRF_COOKIE_SECURE              = False
# SECURE_HSTS_SECONDS             = None
# SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
# SECURE_FRAME_DENY               = False



# –––––––––––––––––––--------------------––#
#    AZZMIN CUSTOM ADMIN PANEL SETTINGS    #
# ––––––––––––––––––--------------------–––#

JAZZMIN_SETTINGS = {
    "site_title": "FinFlo Admin Panel",
    "site_header": "FinFlo Admin Panel",
    "site_brand": "FinFlo Admin Panel",
    "welcome_sign": "Welcome to FinFlo",
    "copyright": "Venzo tech",
    "search_model": "accounts.User",
    "site_logo_classes": "img-circle",
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://github.com/venzo-tech/scfbackend/blob/master/SUPPORT.md", "new_window": True},
    ],
    "site_logo": "images/finflo.png",
    "site_icon": "images/finflo.png",
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "icons": {
        "accounts.user": "fas fa-users",
        "accounts.countries": "fas fa-globe",
        "accounts.banks": "fas fa-university",
        "accounts.parties": "fas fa-building",
        "accounts.signatures": "fas fa-id-card",
        "accounts.userprocessauth": "fas fa-lock",
        "accounts.Currencies": "fas fa-money-bill",
        "accounts.action": "fas fa-bolt",
        "accounts.models": "fas fa-cube",
        "transaction.fundingrequest" : "fas fa-piggy-bank",
        "transaction.invoices": "fas fa-file-invoice",
        "transaction.invoiceuploads": "fas fa-upload",
        "transaction.pairings": "fas fa-cube",
        "transaction.programs": "fas fa-file-invoice",
        "transaction.workevents": "fas fa-file-invoice",
        "transaction.workflowitems": "fas fa-file-invoice",
    },
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-navy",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
}


# –––––––––– END OF JAZZMIN SETTINGS ––––––––––#




