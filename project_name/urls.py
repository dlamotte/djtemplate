from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from {{ project_name }}.core.forms import BootstrapAuthForm

admin.autodiscover()

def handler500(request):
    # for sentry
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({'request': request})))

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^account/login/$', 'login', {
        'authentication_form': BootstrapAuthForm,
    }),
    url(r'^account/logout/$', 'logout'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^humans.txt$', 'direct_to_template', {
        'template': 'humans.txt',
        'mimetype': 'text/plain',
    }),
    url(r'^robots.txt$', 'direct_to_template', {
        'template': 'robots.txt',
        'mimetype': 'text/plain',
    }),
)

# serve static files if proxy doesn't handle them
urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        dict(document_root=settings.MEDIA_ROOT),
    ),
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],
        'django.contrib.staticfiles.views.serve',
    ),
)

urlpatterns += patterns('',
    url('^', include('{{ project_name }}.core.urls')),
)
