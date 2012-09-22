from {{ project_name }}.conf.settings.default import *

TEMPLATE_DEBUG = DEBUG = False

COMPRESS_ENABLED = True

CACHES['default'].update({
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'LOCATION': '127.0.0.1:11211',
    'TIMEOUT': 500,
    'BINARY': True,
    'OPTIONS': {
        'tcp_nodelay': True,
        'ketama': True
    }
})
