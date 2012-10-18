from django.conf.urls import patterns, include, url
from {{ project_name }}.core.apiv1 import api as apiv1

urlpatterns = patterns('{{ project_name }}.core.views',
    url(r'^api/', include(apiv1.urls)),
    url(r'^', 'home', name='home'),
)
