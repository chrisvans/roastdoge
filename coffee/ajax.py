from django.http import JsonResponse

import models


def coffee_delete(request):

    models.Coffee.objects.filter(id=request.POST.get('coffeeID')).delete()

    return JsonResponse({})