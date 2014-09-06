# Django
from django.http import JsonResponse
from django.template.loader import render_to_string

# Ours
import models
import forms

# Third Party
import simplejson


def roastprofile_create(request):
    from coffee import models as coffee_models
    coffee = coffee_models.Coffee.objects.get(id=request.POST.get('coffeeID'))
    roastprofile = models.RoastProfile.objects.create(name='%s%s' % (coffee.name, ' New Profile'), coffee=coffee)

    data = {
        'RoastProfileID': roastprofile.id,
        'roastProfileGraphData': simplejson.loads(roastprofile.get_temp_graph_data_JSON()),
    }

    return JsonResponse(data)

def roastprofile_graph_data_slice(request):

    roastprofile_id = request.GET.get('roastProfileID')
    roastprofile = models.RoastProfile.objects.get(id=roastprofile_id)

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