from dj_database_url import config as config_url
from django.core.urlresolvers import reverse_lazy
from os import path

PROJECT_NAME = PROJECT_NAME_TITLE = '{{ project_name|title }}'
PROJECT_ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
SANDBOX_ROOT = path.dirname(PROJECT_ROOT)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DATABASES = {
    'default': config_url(default='postgres://localhost/{{ project_name }}'),
}
DATABASES['default'].update({
    'OPTIONS': {
        'autocommit': True,
    }
})

TEMPLATE_DEBUG = DEBUG = True

ADMINS = MANAGERS = ()
#COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = 'cache'
LANGUAGE_CODE = 'en-us'
LOGIN_URL = reverse_lazy('django.contrib.auth.views.login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_REDIRECT_TO_CURRENT_PAGE = True
LOGOUT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_TO_CURRENT_PAGE = True
MEDIA_ROOT = path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
GOOGLE_ANALYTICS_KEY = ''
ROOT_URLCONF = '{{ project_name }}.urls'
SECRET_KEY = '{{ secret_key }}'
#SESSION_COOKIE_AGE = 30 * 24 * 60 * 60
#SESSION_COOKIE_SECURE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SITE_ID = 1
STATIC_ROOT = path.join(PROJECT_ROOT, '_static')
STATIC_URL = '/static/'
TIME_ZONE = 'America/Chicago'
USE_I18N = False
USE_L10N = False
USE_TZ = True
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc --include-path="%s" {infile} {outfile}' \
        % path.join(SANDBOX_ROOT, 'deps', 'bootstrap', 'less')),
)

STATICFILES_DIRS = (
    path.join(PROJECT_ROOT, 'static'),
)
TEMPLATE_DIRS = (
    path.join(PROJECT_ROOT, 'templates'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'debug_toolbar',
    'compressor',
    'jsonfield',
    'raven.contrib.django',
    'south',

    '{{ project_name }}.core',
)

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    '{{ project_name }}.core.context_processors.default',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'celery.worker.job': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

# djdt
def show_toolbar(request):
    from django.conf import settings

    if 'MSIE' in request.META.get('HTTP_USER_AGENT', 'MSIE'):
        return False

    user = getattr(request, 'user', None)
    if user \
       and user.is_authenticated() \
       and user.is_staff \
       and (settings.DEBUG or request.GET.has_key('djdt')):
        return True

    return False

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
