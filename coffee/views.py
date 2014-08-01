# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import Http404, HttpResponseRedirect
from django.views import generic

# Ours
import models
import forms


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


class CoffeeList(generic.ListView):
    """
    Responsible for showing all of the relevant Coffees,
    and providing links to the list view of profiles associated with them.
    """

    template_name = 'coffee/coffee_list.jade'
    model = models.Coffee


class CoffeeRoastProfileList(generic.ListView):
    """
    Responsible for showing all of the relevant Roast Profiles, 
    and providing links to their detail view.
    """

    template_name = 'coffee/coffeeroastprofile_list.jade'
    model = models.Coffee

    def get_queryset(self):

        try:
            queryset = self.model._default_manager.get(id=self.kwargs['coffee_id']).roastprofile_set.all()
        except ObjectDoesNotExist:
            raise Http404

        return queryset

