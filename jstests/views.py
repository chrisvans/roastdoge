from django.shortcuts import render

from profiling import views as profiling_views
from profiling import models as profiling_models
from profiling import factories as profiling_factories


class TestRoastProfileDetail(profiling_views.RoastProfileDetail):

    template_name = 'jstests/test_roastprofile_detail.jade'

    def setUp(self):
        self.roastprofile = profiling_factories.RoastProfileFactory()

    def get_object(self, queryset=None):

        self.setUp()

        self.kwargs.update({'roastprofile_id': self.roastprofile.id})
        return super(TestRoastProfileDetail, self).get_object(queryset)

