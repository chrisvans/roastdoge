# Django
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Third Party
from rest_framework import routers

# Ours
import coffee
import profiling


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('profiling.urls')),
    url(r'^coffee/', include('coffee.urls')),
)

# DJANGO REST FRAMEWORK

router = routers.DefaultRouter()
router.register(r'roastprofile', profiling.views.RoastProfileViewSet, base_name='rest-roastprofile')
router.register(r'temppoint', profiling.views.TempPointViewSet, base_name='rest-temppoint')
router.register(r'pointcomment', profiling.views.PointCommentViewSet, base_name='rest-pointcomment')
router.register(r'coffee', coffee.views.CoffeeViewSet, base_name='rest-coffee')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += staticfiles_urlpatterns()