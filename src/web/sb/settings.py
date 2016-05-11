# Django settings for sb project.
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  ('Matt Olson', 'molson@rubycloud.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['api.switchboard.org']

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.environ.get('DB_NAME', ''),                      # Or path to database file if using sqlite3.
        'USER': os.environ.get('DB_USER', ''),                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('DB_PASS', ''),                  # Not used with sqlite3.
        'HOST': os.environ.get('DB_HOST', ''),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.environ.get('DB_PORT', ''),                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/apps/switchboard/current/src/web/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(e@=a038xkmg@gf(o(p3dzz2iue65%vt16g2qk@%ta)1uiyfly'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sb.http.JSONMiddleware'
]

ROOT_URLCONF = 'sb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'sb.healthworker',
    'ajax_select',
    'gunicorn',
    #'south' # not needed for django version 1.9
)

# define the lookup channels for ajax_select
AJAX_LOOKUP_CHANNELS = {
  'facility' : {'model': 'healthworker.Facility', 'search_field': 'title'}
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
      'format': '%(asctime)s %(module)s %(levelname)s %(process)d %(thread)d %(message)s'
    },
    'simple': {
      'format': '%(levelname)s %(message)s'
    },
  },
  'handlers': {
    'app': {
      'level': os.environ.get('APP_LOG_LEVEL', 'ERROR'),
      'class': 'logging.FileHandler',
      'formatter': 'verbose',
      'filename': os.environ.get('APP_LOG_PATH', 'app.log')}
  },
  'loggers': {
    'sb': {
      'handlers': ['app'],
      'level': 'DEBUG',
      'propagate': False
    },
    '': {
      'handlers': ['app'],
      'level': 'ERROR'
    }
  }
}

# VUMI GO SMS Settings

VUMIGO_API_URL = os.environ.get('VUMIGO_API_URL')
VUMIGO_CONVERSATION_ID = os.environ.get('VUMIGO_CONVERSATION_ID')
VUMIGO_CONVERSATION_TOKEN = os.environ.get('VUMIGO_CONVERSATION_TOKEN')
VUMIGO_ACCOUNT_ID = os.environ.get('VUMIGO_ACCOUNT_ID')
VUMIGO_SEND_SMSES = bool(VUMIGO_API_URL)
