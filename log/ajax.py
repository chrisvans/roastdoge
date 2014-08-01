# Django
from django.http import HttpResponse
import simplejson


def temppoint_comment_create(request):

    return HttpResponse(simplejson.dumps({}))


def comment_update(request):

    return HttpResponse(simplejson.dumps({}))
