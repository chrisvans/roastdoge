# Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import JsonResponse
from django.shortcuts import Http404, HttpResponseRedirect, HttpResponse, render
from django.template.loader import render_to_string
from django.views import generic

# Ours
import forms
import models
import serializers

# Third Party
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
import simplejson


class PointCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows for pointcomments to be viewed or edited.
    """

    queryset = models.PointComment.objects.all()
    serializer_class = serializers.PointCommentSerializer

    @detail_route(methods=['delete'])
    def delete_and_respond(self, request, pk=None):
        """
        Method to delete a comment, and return JSON containing 
        to the comment's ID, and whether or not the temppoint 
        has any remaining comments.

        JsonResponse:
            {
                'deletedCommentID':pk, 
                'hasComments': point.pointcomment_set.all().exists()
            }
        """

        pointcomment = models.PointComment.objects.get(id=pk)
        point = pointcomment.point
        pointcomment.delete()
        has_comments = point.pointcomment_set.all().exists()

        return JsonResponse({'deletedCommentID':pk, 'hasComments': has_comments})

    @list_route(methods=['get'])
    def get_form(self, request, pk=None):
        """
        Method to get a new comment form, and all previous comments for a given 
        temppoint.
        """

        temppoint_id = request.GET.get('id')

        temppoint = models.TempPoint.objects.get(id=temppoint_id)
        form = forms.PointCommentForm(data={'point':temppoint_id})
        comments = temppoint.pointcomment_set.all().order_by('created')

        data = render_to_string('_includes/forms/point_comment_form.jade', {
            'point':temppoint,
            'form':form,
            'comments': comments,
            }
        )

        return JsonResponse({'data':data})


class RoastProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows roastprofiles to be viewed or edited.
    """

    queryset = models.RoastProfile.objects.all()
    serializer_class = serializers.RoastProfileSerializer

    @list_route(methods=['get'])
    def get_graph_data_slice(self, request, pk=None):
        """
        API endpoint that allows a slice of a roastprofile's graph data to be grabbed.

        GET: 
            'sliceStart': A number corresponding to the time to start the slice from.

        Currently only supports slicing from a certain point all the way to the end.  There 
        is no 'sliceEnd' implementation.
        """

        roastprofile = models.RoastProfile.objects.get(id=request.GET.get('id'))

        slice_start = request.GET.get('sliceStart')

        def get_lastslice_or_zero():
            if roastprofile.temppoint_set.all().exists():
                return roastprofile.temppoint_set.all().order_by('-time')[0].time
            else:
                return 0

        data = {
            'graphDataValues': roastprofile.get_temp_graph_data_slice(slice_start),
            'lastSlice': get_lastslice_or_zero(),
        }

        return JsonResponse(data)


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