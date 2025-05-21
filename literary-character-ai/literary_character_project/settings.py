# literary_character_project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv()

# --- Core Settings ---
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-insecure-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Define allowed hosts. '*' is insecure for production.
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # For the API endpoints
    'characters',     # The main application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Manages sessions across requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Cross-Site Request Forgery protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Associates users with requests using sessions
    'django.contrib.messages.middleware.MessageMiddleware', # For flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking protection
]

ROOT_URLCONF = 'literary_character_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Look for base templates here
        'APP_DIRS': True, # Look for templates within app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Adds HttpRequest to context
                'django.contrib.auth.context_processors.auth', # Adds user, perms to context
                'django.contrib.messages.context_processors.messages', # Adds messages context
            ],
        },
    },
]

WSGI_APPLICATION = 'literary_character_project.wsgi.application'


# --- Database ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # Simple SQLite DB for development
    }
}


# --- Password Validation ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- Internationalization ---
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True # Use timezone-aware datetimes


# --- Static and Media Files ---
# Static files (CSS, JavaScript, Images served directly)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # Directories to find static files
STATIC_ROOT = BASE_DIR / 'staticfiles' # Directory where collectstatic gathers files for production

# Media files (User-uploaded content)
# https://docs.djangoproject.com/en/5.2/topics/files/
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # Directory where user uploads are stored


# --- Primary Key Type ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- API Keys ---
# GROQ_API_KEY is loaded via load_dotenv() and used directly by the groq library instance in api.py
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') # No longer needed


# --- Django REST Framework ---
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    # Using AllowAny for now; tighten permissions as needed, e.g., IsAuthenticated
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


# --- Authentication Settings ---
# URL to redirect to after successful login
LOGIN_REDIRECT_URL = '/app/'
# LOGOUT_REDIRECT_URL = '/' # Commented out; handled by CustomLogoutView's template/JS

# Custom authentication backend for email login
AUTHENTICATION_BACKENDS = [
    'characters.backends.EmailBackend', # Use our email backend first
    'django.contrib.auth.backends.ModelBackend', # Keep default backend for admin login etc.
]


# --- Logging Configuration (Optional but Recommended) ---
# Example basic logging setup - configure further as needed
# https://docs.djangoproject.com/en/5.2/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', # Set to 'DEBUG' for more verbose output during development
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'characters': { # Specific logger for your app
             'handlers': ['console'],
             'level': 'DEBUG' if DEBUG else 'INFO', # More detail from your app in debug mode
             'propagate': False,
        },
    },
}

