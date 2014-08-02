from django.conf.urls import patterns, url

import views, ajax


urlpatterns = patterns('',
    url(r'^/?$', views.index, name='index'),
    url(r'^profiles/(?P<roastprofile_id>\d+)/$', views.RoastProfileDetail.as_view(), name='roastprofile-detail'),
    url(r'^profiles/(?P<roastprofile_id>\d+)/delete/$', views.roastprofile_deleteview, name='roastprofile-delete'),

    # Ajax
    url(
        r'^temppoint/comment/create-form/$', 
        ajax.temppoint_comment_create_form, 
        name='ajax-temppoint-comment-create-form'
    ),
    url(
        r'^temppoint/comment/create/$',
        ajax.temppoint_comment_create,
        name='ajax-temppoint-comment-create'
    ),
    url(r'^temppoint/comment/update/$',
        ajax.comment_update,
        name='ajax-comment-update'
    ),
    url(r'^temppoint/comment/delete/$',
        ajax.comment_delete,
        name='ajax-comment-delete'
    ),
)