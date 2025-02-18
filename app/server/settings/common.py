"""
Django settings for zosia16 project.

Generated by 'django-admin startproject'

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import io
import os
import random
import string

from django.conf.global_settings import DATETIME_INPUT_FORMATS
from dotenv import load_dotenv
from google.cloud import secretmanager
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import django_stubs_ext

# Required for reactivated
django_stubs_ext.monkeypatch()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(env_file):
    load_dotenv(env_file)
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    load_dotenv(stream=io.StringIO(payload))

# Google API key
GAPI_KEY = os.environ.get("GAPI_KEY")

ENV = os.environ.get("DJANGO_ENV", "dev")

# https://security.stackexchange.com/a/175540
# In our case React apps need this token
CSRF_COOKIE_HTTPONLY = False


# SECURITY WARNING: keep the secret key used in production secret!
def random_string(length=10):
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


SECRET_KEY = os.environ.get("SECRET_KEY", random_string(20))

if "SECRET_KEY" not in os.environ:
    os.environ["SECRET_KEY"] = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get("HOSTS", "staging.zosia.org").split(",")
CSRF_TRUSTED_ORIGINS = [f"https://*.{host}" for host in ALLOWED_HOSTS]

AUTH_USER_MODEL = "users.User"

# Anymail docs (https://anymail.dev/en/stable/quickstart/ / https://github.com/anymail/django-anymail)
ANYMAIL = {
    "MAILJET_API_KEY": os.environ.get("MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY": os.environ.get("MAILJET_SECRET_KEY")
}

EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
DEFAULT_FROM_EMAIL = "admin@zosia.org"
DEFAULT_FROM_EMAIL_NAME = "Zosia Administrators"
DEFAULT_MAIL = f"{DEFAULT_FROM_EMAIL_NAME} <{DEFAULT_FROM_EMAIL}>"

sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn is not None:
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=ENV,
        integrations=[DjangoIntegration(
            # Additional settings for Django Integration
            # https://docs.sentry.io/platforms/python/guides/django/#options
        )],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Django REST framework (https://www.django-rest-framework.org)
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Application definition

INSTALLED_APPS = [
    "materializecssform",
    "anymail",
    "rest_framework",
    "drf_yasg",
    "server.blog.apps.BlogConfig",
    "server.boardgames.apps.BoardgameConfig",
    "server.conferences.apps.ConferencesConfig",
    "server.lectures.apps.LecturesConfig",
    "server.organizers.apps.OrganizersConfig",
    "server.questions.apps.QuestionsConfig",
    "server.sponsors.apps.SponsorsConfig",
    "server.rooms.apps.RoomsConfig",
    "server.users.apps.UsersConfig",
    "server.utils.apps.UtilsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "reactivated",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "server.utils.www_redirect.NoWWWRedirectMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "server", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "reactivated.backend.JSX",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.csrf",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "server.utils.context_processors.user_context",
                "server.utils.context_processors.server_time_context",
                "server.utils.context_processors.recaptcha_context",
            ]
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "zosia",
        "USER": "zosia",
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# List of hashing algorithm classes
# https://docs.djangoproject.com/en/2.2/topics/auth/passwords/
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_FORMAT = "Y-m-d"

TIME_FORMAT = "H:i"

# ISO 8601 datetime format to accept html5 datetime input values
DATETIME_INPUT_FORMATS += ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = "/static"
STATICFILES_DIRS = ['/code/static']
