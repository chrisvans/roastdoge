# Django
from django.http import JsonResponse
from django.template.loader import render_to_string

# Ours
import models
import forms


def temppoint_comment_create_form(request):

    temppoint_id = request.GET.get('TempPointID')

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


def temppoint_comment_create(request):

    temppoint = models.TempPoint.objects.get(id=request.POST.get('TempPointID'))
    comment = request.POST.get('comment')

    comment = models.PointComment.objects.create(point=temppoint, comment=comment)

    return JsonResponse({})


def comment_update(request):

    return JsonResponse({})


def comment_delete(request):

    temppoint = models.TempPoint.objects.get(id=request.POST.get('TempPointID'))
    temppoint.pointcomment_set.get(id=request.POST.get('commentID')).delete()

    data = {
        'deletedCommentID': request.POST.get('commentID'),
        'hasComments': temppoint.pointcomment_set.all().exists()
    }

    return JsonResponse(data)

def roastprofile_create(request):
    from coffee import models as coffee_models
    coffee = coffee_models.Coffee.objects.get(id=request.POST.get('coffeeID'))
    roastprofile = models.RoastProfile.objects.create(name='%s%s' % (coffee.name, ' New Profile'), coffee=coffee)

    data = {
        'RoastProfileID': roastprofile.id,
        'roastProfileGraphData': roastprofile.get_temp_graph_data(),
    }

    return JsonResponse(data)

def roastprofile_delete(request):

    models.RoastProfile.objects.get(id=request.POST.get('RoastProfileID')).delete()

    data = {
    }
    
    return JsonResponse(data)

def roastprofile_graph_data(request):

    roastprofile_id = request.GET.get('roastProfileID')
    roastprofile = models.RoastProfile.objects.get(id=roastprofile_id)

    data = {
        'graphData': roastprofile.get_temp_graph_data()
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