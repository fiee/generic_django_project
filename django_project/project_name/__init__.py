#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

verbose_name = _(u'project_name')
verbose_name_plural = _(u'project_names')

# see http://djangopatterns.com/patterns/app_construction/version_reporting/
__version_info__ = {
    'major': 0,
    'minor': 0,
    'micro': 1,
    'releaselevel': 'alpha',
    'serial': 1
}

def get_version(short=False):
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()
