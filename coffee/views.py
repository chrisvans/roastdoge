# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import Http404, HttpResponseRedirect
from django.views import generic

# Ours
import models
import forms
import serializers
from object_utils.views import ObjectDataMixin
from profiling import models as profiling_models

# Third Party
from rest_framework import viewsets


class CoffeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows coffees to be viewed or edited.
    """
    queryset = models.Coffee.objects.all()
    serializer_class = serializers.CoffeeSerializer


class GreenCoffeeCreate(generic.FormView):
    """
    Responsible for rendering a form for a GreenCoffee,
    processing a post from that form, and creating a new
    GreenCoffee.
    """

    template_name = 'coffee/coffee_create.jade'
    form_class = forms.GreenCoffeeForm
    success_url = reverse_lazy('coffee-list')

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect(self.get_success_url())


class CoffeeCreate(generic.FormView):
    """
    Responsible for rendering a form for a Coffee,
    processing a post from that form, and creating a new
    Coffee.
    """

    template_name = 'coffee/coffee_create.jade'
    form_class = forms.CoffeeForm
    success_url = reverse_lazy('coffee-list')

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect(self.get_success_url())


class CoffeeList(generic.ListView, ObjectDataMixin):
    """
    Responsible for showing all of the relevant Coffees,
    and providing links to the list view of profiles associated with them.
    """

    template_name = 'coffee/coffee_list.jade'
    model = models.Coffee


class CoffeeRoastProfileList(generic.ListView, ObjectDataMixin):
    """
    Responsible for showing all of the relevant Roast Profiles, 
    and providing links to their detail view.
    """

    template_name = 'coffee/coffeeroastprofile_list.jade'
    model = profiling_models.RoastProfile

    def get_queryset(self):

        try:
            queryset = self.model._default_manager.filter(coffee__id=self.kwargs['coffee_id'])
        except ObjectDoesNotExist:
            raise Http404

        return queryset

