from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('profiling.urls')),
    url(r'^coffee/', include('coffee.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'jstests.views',
        url(r'^tests/', include('jstests.urls')),
    )

urlpatterns += staticfiles_urlpatterns()