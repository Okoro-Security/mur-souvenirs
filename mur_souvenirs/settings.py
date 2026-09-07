from pathlib import Path


# =========================================================
# BASE DU PROJET
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SÉCURITÉ
# =========================================================

import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-key-change-me")

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if render_host:
    ALLOWED_HOSTS.append(render_host)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "axes",
    "souvenirs",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS
# =========================================================

ROOT_URLCONF = "mur_souvenirs.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# SERVEUR
# =========================================================

WSGI_APPLICATION = "mur_souvenirs.wsgi.application"


# =========================================================
# BASE DE DONNÉES
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================================================
# VALIDATION DES MOTS DE PASSE
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================================================
# LANGUE
# =========================================================

LANGUAGE_CODE = "fr-fr"


# =========================================================
# FUSEAU HORAIRE
# =========================================================

TIME_ZONE = "Africa/Lome"

USE_I18N = True
USE_TZ = True


# =========================================================
# FICHIERS STATIQUES
# =========================================================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# =========================================================
# FICHIERS MÉDIA
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# ID AUTOMATIQUE
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],

    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}







AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1








STATIC_ROOT = BASE_DIR / 'staticfiles'
