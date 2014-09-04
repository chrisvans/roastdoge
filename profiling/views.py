# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import Http404, HttpResponseRedirect, HttpResponse, render
from django.views import generic

# Ours
import models
import serializers

# Third Party
from rest_framework import viewsets


class RoastProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows roastprofiles to be viewed or edited.
    """
    queryset = models.RoastProfile.objects.all()
    serializer_class = serializers.RoastProfileSerializer


class TempPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows temppoints to be viewed or edited.
    """
    queryset = models.TempPoint.objects.all()
    serializer_class = serializers.TempPointSerializer


def index(request):
	return render(request, 'index.jade')


class RoastProfileDetail(generic.DetailView):
    """
    Responsible for showing a single roast profile's information 
    along with a line chart ( the roast profile temp/time ) created 
    from all of the associated TempPoint objects.
    """

    template_name = 'profiling/roastprofile_detail.jade'
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


# TODO: Properly use POST instead of GET for this.
def roastprofile_temppoint_create(request, roastprofile_id):
 
    roastprofile = models.RoastProfile.objects.get(id=roastprofile_id)
    time = request.GET.get('time')
    temperature = request.GET.get('temperature')

    models.TempPoint.objects.create(roast_profile=roastprofile, time=time, temperature=temperature)

    return HttpResponse()