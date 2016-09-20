from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject


def site(request):
    return {
        'host': request.META['HTTP_HOST'],
        'site': SimpleLazyObject(lambda: get_current_site(request)),
    }
