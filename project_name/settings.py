from {{ project_name }}.conf.settings.default import *

TEMPLATE_DEBUG = DEBUG = False

COMPRESS_ENABLED = True

CACHES['default'].update({
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
})
