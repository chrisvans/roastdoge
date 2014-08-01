# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import Http404, HttpResponseRedirect, render
from django.views import generic

# Ours
import models


def index(request):
	return render(request, 'index.jade')


class RoastProfileDetail(generic.DetailView):
    """
    Responsible for showing a single roast profile's information 
    along with a line chart ( the roast profile temp/time ) created 
    from all of the associated TempPoint objects.
    """

    template_name = 'log/roastprofile_detail.jade'
    model = models.RoastProfile
    pk_url_kwarg = 'roastprofile_id'


def roastprofile_deleteview(request, roastprofile_id):
    """
    Responsible for deleting a roast profile based on the id that 
    is passed in.  Then renders the roastprofile list view.
    """

    # TODO - Decide what to do on failure.  Give error message and redirect to coffee-list ?
    roastprofile = models.RoastProfile.objects.get(id=roastprofile_id)
    coffee = roastprofile.coffee
    roastprofile.delete()

    return HttpResponseRedirect(reverse('coffeeroastprofile-list', kwargs={'coffee_id': coffee.id}))