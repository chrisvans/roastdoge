# Django
from django.conf.urls import patterns, url, include 

# Ours
import views, ajax

# Third Party
from rest_framework import routers


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
    url(r'^roastprofile/temppoint/get-graph-data/$',
        ajax.roastprofile_graph_data,
        name='ajax-roastprofile-graph-data'
    ),
    url(r'^roastprofile/temppoint/get-graph-data-slice/$',
        ajax.roastprofile_graph_data_slice,
        name='ajax-roastprofile-graph-data-slice'
    ),
    url(r'^roastprofile/create/$',
        ajax.roastprofile_create,
        name='ajax-roastprofile-create'
    ),
    url(r'^roastprofile/delete/$',
        ajax.roastprofile_delete,
        name='ajax-roastprofile-delete'
    ),
)


# DJANGO REST FRAMEWORK

router = routers.DefaultRouter()
router.register(r'roastprofile', views.RoastProfileViewSet, base_name='rest-roastprofile')
router.register(r'temppoint', views.TempPointViewSet, base_name='rest-temppoint')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

