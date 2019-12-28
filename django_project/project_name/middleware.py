#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# A simple middleware component that lets you use a single Django
# instance to server multiple distinct hosts.
# inspired by http://effbot.org/zone/django-multihost.htm
##
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.cache import patch_vary_headers
# from django.contrib.sites.models import Site
from django.utils.deprecation import MiddlewareMixin
import logging
logger = logging.getLogger(__name__)


class MultiHostMiddleware(MiddlewareMixin):
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

        # optional host dependend email settings
        HOST_EMAIL = {
            'default': {
                'backend': 'django.core.mail.backends.smtp.EmailBackend',
                'host': 'mail.example.com',
                'host_user': EMAIL_HOST_USER,
                'host_password': EMAIL_HOST_PASSWORD,
                'port': EMAIL_PORT,
                'use_tls': EMAIL_USE_TLS,
                'default_from_email': DEFAULT_FROM_EMAIL,
                'server_email': SERVER_EMAIL,
                'subject_prefix': EMAIL_SUBJECT_PREFIX
                },
            'localhost': {
                'backend': 'django.core.mail.backends.console.EmailBackend',
                },
            'example.com': {
                'server_email': 'webserver@example.com',
                'host_user': 'webserver@example.com',
                'host_password': get_env_variable('EMAIL_PASSWORD_EXAMPLECOM'),
                'subject_prefix': '[EXAMPLE]',
                },
            'example.de': {},
            'otherdomain.com': {},
        }

    See also https://github.com/fiee/generic_django_project/wiki/MultiHostMiddleware
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
        try:
            if 'HOST_EMAIL' in settings:
                mail_settings = settings.HOST_EMAIL['default']
                host_settings = settings.HOST_EMAIL[host]
                for key in host_settings:
                    mail_settings[key] = host_settings[key]
                for key in ('backend', 'host', 'host_user', 'host_password', 'port', 'use_tls', 'subject_prefix'):
                    if key in mail_settings:
                        setattr(settings, 'EMAIL_' + key.upper(), mail_settings[key])
                for key in ('server_email', 'default_from_email'):
                    if key in mail_settings:
                        setattr(settings, key.upper(), mail_settings[key])
        except KeyError as ex:
            logger.error('MultiHostMiddleware: Missing setting in HOST_EMAIL')
            logger.exception(ex)

        if not settings.SITE_ID:
            settings.SITE_ID = 1

    def process_response(self, request, response):
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response
