# Django
from django.http import HttpResponse
from django.template.loader import render_to_string

# Ours
import models
import forms

# Third Party
import simplejson


def temppoint_comment_create_form(request):

    temppoint_id = request.GET.get('tempPointID')

    temppoint = models.TempPoint.objects.get(id=temppoint_id)
    form = forms.PointCommentForm(data={'point':temppoint_id})
    comments = temppoint.pointcomment_set.all().order_by('created')

    data = render_to_string('_includes/forms/point_comment_form.jade', {
        'point':temppoint,
        'form':form,
        'comments': comments,
        }
    )

    return HttpResponse(simplejson.dumps({'data':data}))


def temppoint_comment_create(request):

    temppoint = models.TempPoint.objects.get(id=request.POST.get('tempPointID'))
    comment = request.POST.get('comment')

    comment = models.PointComment.objects.create(point=temppoint, comment=comment)

    return HttpResponse(simplejson.dumps({}))


def comment_update(request):

    return HttpResponse(simplejson.dumps({}))


def comment_delete(request):

    temppoint = models.TempPoint.objects.get(id=request.POST.get('tempPointID'))
    temppoint.pointcomment_set.get(id=request.POST.get('commentID')).delete()

    data = {
        'deletedCommentID': request.POST.get('commentID'),
        'hasComments': temppoint.pointcomment_set.all().exists()
    }

    return HttpResponse(simplejson.dumps(data))

def roastprofile_create(request):
    from coffee import models as coffee_models
    coffee = coffee_models.Coffee.objects.get(id=request.POST.get('coffeeID'))
    roastprofile = models.RoastProfile.objects.create(name='%s%s' % (coffee.name, ' New Profile'), coffee=coffee)

    data = {
        'roastProfileID': roastprofile.id,
        'roastProfileGraphData': roastprofile.get_temp_graph_data(),
    }

    return HttpResponse(simplejson.dumps(data))

def roastprofile_delete(request):

    models.RoastProfile.objects.get(id=request.POST.get('roastProfileID')).delete()

    data = {
        'deletedRoastProfileID': request.POST.get('roastProfileID')
    }
    
    return HttpResponse(simplejson.dumps(data))

def roastprofile_graph_data(request):

    roastprofile_id = request.GET.get('roastProfileID')
    roastprofile = models.RoastProfile.objects.get(id=roastprofile_id)

    data = {
        'graphData': roastprofile.get_temp_graph_data()
    }

    return HttpResponse(simplejson.dumps(data))
