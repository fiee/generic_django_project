from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from feincms.module.page.models import Page
# from feincms.module.page.sitemap import PageSitemap
import os
from django.views.generic import TemplateView, ListView

admin.autodiscover()

#mysitemaps = {
#    'page' : GenericSitemap({
#        'queryset': Page.objects.all(),
#        'changefreq' : 'monthly',
#        'date_field': 'modification_date',
#    }, priority=0.6),
#}
## OR
# mysitemaps = {'pages' : PageSitemap}

urlpatterns = [
        (r'', TemplateView.as_view(template_name="root.html")),
]

# serve static content in debug mode
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
            'show_indexes': True
        }),
        url(r'^(media/|static/)?medialibrary/(?P<path>.*)$',
            'django.views.static.serve', {
            'document_root': '%s/medialibrary/' % settings.MEDIA_ROOT,
            'show_indexes': True
        }),
        url(r'^(?P<path>favicon.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ]


urlpatterns += [
    # (r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', admin.site.urls),    
    # url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': mysitemaps}),
    # FeinCMS 1.12- sitemaps don’t work with Django 1.10+
    # url(r'', include('feincms.urls')),
]
