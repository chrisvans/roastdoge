# Django
from django.conf.urls import patterns, url, include 

# Ours
import views


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='index'),
    url(
        r'^profiles/(?P<roastprofile_id>\d+)/$', 
        views.RoastProfileDetail.as_view(), 
        name='roastprofile-detail'
    ),
    url(
        r'^profiles/(?P<roastprofile_id>\d+)/delete/$', 
        views.roastprofile_deleteview, 
        name='roastprofile-delete'
    ),
    url(
        r'^roastprofile/(?P<roastprofile_id>\d+)/temppoint/create/$', 
        views.roastprofile_temppoint_create, 
        name='roastprofile-temppoint-create'
    ),
)

