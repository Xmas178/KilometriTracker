"""
Django settings for KilometriTracker project.
CodeNob Dev - Security-first development with comprehensive documentation

This file contains all Django configuration including:
- App registration
- Database configuration
- Security settings
- REST Framework & JWT authentication
- Celery task queue configuration
- Email settings
- Google Maps API integration
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
import os

# Build paths inside the project
# BASE_DIR points to the backend/ directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing - MUST be kept secret in production
# Read from environment variable, fallback to dev key if not set
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-dev-key-change-in-production"
)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG mode shows detailed error pages - useful for development, dangerous in production
DEBUG = config("DEBUG", default=True, cast=bool)

# Allowed hosts - which domains can access this Django app
# In production, set to your actual domain names
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# Application definition
# INSTALLED_APPS tells Django which applications to use
INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",  # Admin panel at /admin
    "django.contrib.auth",  # Authentication system
    "django.contrib.contenttypes",  # Content type system
    "django.contrib.sessions",  # Session management
    "django.contrib.messages",  # Messaging framework
    "django.contrib.staticfiles",  # Static file management
    # Third party apps
    "rest_framework",  # Django REST Framework for API
    "rest_framework_simplejwt",  # JWT authentication
    "corsheaders",  # CORS headers for frontend communication
    "django_filters",  # Filtering querysets in API
    "django_celery_beat",  # Periodic tasks (monthly reports)
    # Local apps - our custom applications
    "apps.users",  # User management and authentication
    "apps.trips",  # Trip entry and management
    "apps.reports",  # Monthly report generation
]

# Middleware - components that process requests/responses
# Order matters! Each request passes through middleware from top to bottom
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security enhancements
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files efficiently
    "corsheaders.middleware.CorsMiddleware",  # CORS - MUST be before CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session support
    "django.middleware.common.CommonMiddleware",  # Common utilities
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # User authentication
    "django.contrib.messages.middleware.MessageMiddleware",  # Messages framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
]

# URL configuration - main URL router
ROOT_URLCONF = "config.urls"

# Template configuration
# Django templates for rendering HTML (if needed)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Additional template directories
        "APP_DIRS": True,  # Look for templates in app directories
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application - used by production servers like gunicorn
WSGI_APPLICATION = "config.wsgi.application"

# Database configuration
# Development: SQLite (file-based database)
# Production: PostgreSQL (set via DATABASE_URL environment variable)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Override database settings in production
# Uses dj-database-url to parse DATABASE_URL environment variable
if not DEBUG:
    import dj_database_url

    DATABASES["default"] = dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,  # Keep database connections alive for 10 minutes
    )

# Password validation
# Ensures users create strong passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        # Prevents passwords too similar to user attributes
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # Requires minimum password length
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,  # At least 8 characters
        },
    },
    {
        # Prevents common passwords like "password123"
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # Prevents entirely numeric passwords
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Custom User Model
# We use a custom User model instead of Django's default
# This allows adding fields like company, phone etc.
AUTH_USER_MODEL = "users.User"

# Internationalization
# Language and timezone settings
LANGUAGE_CODE = "en-us"  # Default language
TIME_ZONE = "Europe/Helsinki"  # Timezone for timestamps
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Use timezone-aware datetimes

# Static files (CSS, JavaScript, Images)
# Configuration for serving static files
STATIC_URL = "static/"  # URL prefix for static files
STATIC_ROOT = BASE_DIR / "staticfiles"  # Where collectstatic gathers files
STATICFILES_DIRS = [BASE_DIR / "static"]  # Additional static file directories
# WhiteNoise storage - compresses and caches static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (User uploads)
# Configuration for user-uploaded files (PDFs, Excel reports)
MEDIA_URL = "media/"  # URL prefix for media files
MEDIA_ROOT = BASE_DIR / "media"  # Directory where media files are stored

# Default primary key field type
# Uses BigAutoField (64-bit integer) for auto-incrementing IDs
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework Configuration
# Settings for our API
REST_FRAMEWORK = {
    # Authentication - how users prove their identity
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT tokens
    ),
    # Permissions - who can access what
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",  # Require login by default
    ),
    # Pagination - split large result sets into pages
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,  # 20 items per page
    # Filtering - allow filtering, searching, and ordering of querysets
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",  # Filter by fields
        "rest_framework.filters.SearchFilter",  # Text search
        "rest_framework.filters.OrderingFilter",  # Sort results
    ),
}

# JWT (JSON Web Token) Configuration
# Settings for authentication tokens
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),  # Access token valid for 1 hour
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh token valid for 7 days
    "ROTATE_REFRESH_TOKENS": True,  # Issue new refresh token on refresh
    "BLACKLIST_AFTER_ROTATION": True,  # Invalidate old refresh tokens
    "UPDATE_LAST_LOGIN": True,  # Update user's last_login field
    "ALGORITHM": "HS256",  # HMAC-SHA256 signing algorithm
    "SIGNING_KEY": SECRET_KEY,  # Use Django SECRET_KEY for signing
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization: Bearer <token>
}

# CORS (Cross-Origin Resource Sharing) Configuration
# Allows frontend (React) to make requests to backend (Django)
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000",  # Development frontend URLs
    cast=lambda v: [s.strip() for s in v.split(",")],
)
CORS_ALLOW_CREDENTIALS = True  # Allow cookies/auth headers in CORS requests

# Security Settings
# Additional security headers - only enabled in production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing
    X_FRAME_OPTIONS = "DENY"  # Prevent clickjacking
    SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
    SESSION_COOKIE_SECURE = True  # Send session cookie only over HTTPS
    CSRF_COOKIE_SECURE = True  # Send CSRF cookie only over HTTPS
    SECURE_HSTS_SECONDS = 31536000  # HSTS - force HTTPS for 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to subdomains
    SECURE_HSTS_PRELOAD = True  # Allow browser HSTS preload

# Celery Configuration
# Distributed task queue for asynchronous tasks (e.g., sending monthly reports)
CELERY_BROKER_URL = config(
    "REDIS_URL", default="redis://localhost:6379/0"
)  # Message broker
CELERY_RESULT_BACKEND = config(
    "REDIS_URL", default="redis://localhost:6379/0"
)  # Result storage
CELERY_ACCEPT_CONTENT = ["json"]  # Accept only JSON serialization
CELERY_TASK_SERIALIZER = "json"  # Serialize tasks as JSON
CELERY_RESULT_SERIALIZER = "json"  # Serialize results as JSON
CELERY_TIMEZONE = TIME_ZONE  # Use same timezone as Django

# Email Configuration
# Settings for sending emails (monthly reports)
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",  # Print emails to console in dev
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")  # SMTP server
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)  # SMTP port
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)  # Use TLS encryption
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # SMTP username
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # SMTP password
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default="noreply@kilometritracker.com"
)

# Google Maps API Configuration
# API key for distance calculation between addresses
GOOGLE_MAPS_API_KEY = config("GOOGLE_MAPS_API_KEY", default="")

# Logging Configuration
# Configure how Django logs messages
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            # Log format: LEVEL TIMESTAMP MODULE MESSAGE
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            # Print logs to terminal
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            # Write logs to debug.log file
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug.log",
            "formatter": "verbose",
        },
    },
    "root": {
        # Root logger - catches all logs
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            # Django framework logs
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            # Our application logs
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
