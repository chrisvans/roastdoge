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

urlpatterns += patterns(
    '',
    url(r'^object/delete', 'object_utils.ajax.object_delete', name='ajax-object-delete')
)

urlpatterns += staticfiles_urlpatterns()