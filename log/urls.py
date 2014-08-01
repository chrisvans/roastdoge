from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='index'),
    url(r'^profiles/(?P<roastprofile_id>\d+)/$', views.RoastProfileDetail.as_view(), name='roastprofile-detail'),
    url(r'^profiles/(?P<roastprofile_id>\d+)/delete/$', views.roastprofile_deleteview, name='roastprofile-delete'),
)