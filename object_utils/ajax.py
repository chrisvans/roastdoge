from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse


def object_delete(request):
    """
    Generic Ajax View for deleting an object.

    Required parameters:
    objectID: A valid object.id
    objectName: The object model's name ex. 'RoastProfile'
    objectModule: The dotted path to the object's module ex. 'profiling.models' 
    """

    object_id = request.POST.get('objectID')
    object_classname = request.POST.get('objectName')
    object_module = request.POST.get('objectModule')

    if not all([object_id, object_classname, object_module]):
        raise ImproperlyConfigured('Ajax request made without proper POST params to object_delete.')

    object_app_label = object_module.split('.')[0]

    object_class = ContentType.objects.get(
        app_label = object_app_label,
        model= object_classname.lower(),
    ).model_class()

    object_class.objects.filter(id=object_id).delete()

    # TODO: Return something useful.
    return JsonResponse({})