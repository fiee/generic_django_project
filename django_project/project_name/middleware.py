##
# A simple middleware component that lets you use a single Django
# instance to server multiple distinct hosts.
# after http://effbot.org/zone/django-multihost.htm
##
from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.cache import patch_vary_headers
# from django.contrib.sites.models import Site
import logging
logger = logging.getLogger(__name__)


class MultiHostMiddleware:
    """
    Changes SITE_ID according to the calling host.

    Use case: You want to serve several domains with the same installation
    of Django (and e.g. FeinCMS).

    You need `HOST_MIDDLEWARE_URLCONF_MAP` in your settings like this::

        HOST_MIDDLEWARE_URLCONF_MAP = collections.OrderedDict((
            ("localhost", "project_name.urls_local"),
            ("example.com", "project_name.urls_com"),
            ("example.de", "project_name.urls_de"),
            ("otherdomain.com", "project_name.urls_other"),
        ))
    """
    def process_request(self, request):
        if 'HOST_MIDDLEWARE_URLCONF_MAP' not in settings:
            text = 'You must setup HOST_MIDDLEWARE_URLCONF_MAP for MultiHostMiddleware!'
            logger.error(text)
            raise ImproperlyConfigured(text)
        try:
            host = request.META["HTTP_HOST"]
            if ':' in host:
                # ignore port number, if present
                host, port = host.split(':')
            if host.startswith('www.'):
                parts = host.split('.')
                host = '.'.join(parts[1:])
            request.urlconf = settings.HOST_MIDDLEWARE_URLCONF_MAP[host]
            settings.SITE_ID = settings.HOST_MIDDLEWARE_URLCONF_MAP.keys().index(host)
        except KeyError as ex:
            logger.error('MultiHostMiddleware: Host "%s" is not in HOST_MIDDLEWARE_URLCONF_MAP' % host)
            logger.exception(ex)
            # use default urlconf (settings.ROOT_URLCONF)
        if not settings.SITE_ID:
            settings.SITE_ID = 1

    def process_response(self, request, response):
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response
