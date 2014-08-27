from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^profiling/roastprofile_detail/', 
        views.TestRoastProfileDetail.as_view(), 
        name='test-roastprofile-detail'
    )
)