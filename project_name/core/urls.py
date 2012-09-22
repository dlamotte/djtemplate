from django.conf.urls import patterns, include, url
from {{ project_name }}.core.api import api as api

urlpatterns = patterns('{{ project_name }}.core.views',
    url(r'^api/', include(api.urls)),
    url(r'^$', 'home', name='home'),
)
