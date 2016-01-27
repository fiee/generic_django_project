#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.loader import render_to_string
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

Page.register_templates({
    'key' : 'base',
    'title': _('Standard template'),
    'path': 'cms_base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
    ),
})

Page.register_extensions(
    'feincms.module.extensions.changedate', # add creation and modification date to pages
    'feincms.module.extensions.datepublisher', # define when pages get visible
    'feincms.module.extensions.translations' # translations
) # Example set of extensions
# consider ct_tracker, if you use more than three content types

Page.create_content_type(RichTextContent)

Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
))
