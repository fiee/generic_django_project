#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.loader import render_to_string
#from django.contrib.markup.templatetags.markup import restructuredtext
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

Page.register_templates(
    {
    'key' : 'base',
    'title': _(u'Standard template'),
    'path': 'cms_base.html',
    'regions': (
        ('main', _(u'Main content area')),
    ),
    },
    )
Page.register_extensions('changedate', 'translations', )

#class ReSTContent(models.Model):
#    content = models.TextField()
#
#    class Meta:
#        abstract = True
#        verbose_name = _(u'ReStructured Text')
#        verbose_name_plural = _(u'ReStructured Texts')
#
#    def render(self, **kwargs):
#        return restructuredtext(self.content)
#Page.create_content_type(ReSTContent)

Page.create_content_type(RichTextContent)
#MediaFileContent.default_create_content_type(Page)
Page.create_content_type(MediaFileContent, POSITION_CHOICES=(
    #('left', _(u'left')),
    ('right', _(u'right')),
    ('center', _(u'center')),
    ))
