#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from feincms.module.page.models import Page
# from feincms.module.page.sitemap import PageSitemap
import os
from django.views.generic import TemplateView, ListView

admin.autodiscover()

# mysitemaps = {
#    'page' : GenericSitemap({
#        'queryset': Page.objects.all(),
#        'changefreq' : 'monthly',
#        'date_field': 'modification_date',
#    }, priority=0.6),
# }
# OR
# mysitemaps = {'pages' : PageSitemap}

urlpatterns = [
    (r'', TemplateView.as_view(template_name="root.html")),
]

# serve static content in debug mode
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        path('admin/doc/', include('django.contrib.admindocs.urls')),
    ] + \
    #static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT) + \
    static('/medialibrary/', document_root=settings.MEDIA_ROOT) + \
    static('/favicon.ico', document_root=settings.MEDIA_ROOT) + \
    static(settings.FEINCMS_ADMIN_MEDIA, document_root=settings.MEDIA_ROOT + '/feincms')


urlpatterns += [
    # path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    # path('sitemap.xml', 'django.contrib.sitemaps.views.sitemap', kwargs={'sitemaps': mysitemaps}, name='sitemap'),
    # FeinCMS 1.12- sitemaps don’t work with Django 1.10+
    # path('', include('feincms.urls')),
]
