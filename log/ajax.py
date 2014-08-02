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

    models.PointComment.objects.get(id=request.POST.get('commentID')).delete()

    return HttpResponse(simplejson.dumps({}))
