# use this as settings.py if you’re writing a reusable app and not a single project
# see http://djangopatterns.com/patterns/configuration/configure_app/
from django.conf import settings

SOME_SETTING = getattr(settings, '%s_SOME_SETTING' % settings.PROJECT_NAME.upper(), 'this')

#if API_KEY is None:
#    raise ImproperlyConfigured("You haven't set '%s_API_KEY'." % settings.PROJECT_NAME.upper())
