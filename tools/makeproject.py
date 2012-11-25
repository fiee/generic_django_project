#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configurator for new Django project, based on fiee's "generic_django_project".

Uses `urwid` (ncurses wrapper/replacement) from http://excess.org/urwid/
"""
import os, sys
import urwid

def _(text):
    return text

palette = [
    ('header', 'dark green', 'black', 'standout'),
    ('footer', 'white', 'dark green', 'standout'),
    ('button', 'white', 'dark cyan', 'underline'),
    ('question', 'default,bold', 'default', 'bold'),
    ('answer', 'dark green', 'default', 'default'),
    ('bg', 'black', 'light gray'),
]

questions = [
    ('project_name', _(u'Name of the project? (same as user on webserver and database!)'), 'project_name'),
    ('project_root', _(u'Local project root?'), '~/workspace/'),
    ('server_domain', _(u'Name of your domain? (without server name)'), 'example.com'),
    ('server_name', _(u'Name of your web server? (without domain name)'), 'www'),
    ('database_type', _(u'Database on server? (mysql, postgresql, sqlite)'), 'mysql'),
    ('webserver', _(u'Webserver software? (apache+mod_wsgi, nginx+gunicorn, nginx+fcgi)'), 'nginx+gunicorn'),
    ('processcontrol', _(u'Process supervision? (daemontools, supervisord'), 'supervisord'),
    ('messagequeue', _(u'Message queue? (celery)'), ''),
    ('modules', _(u'Use special modules? (feincms, medialibrary, photologue, south)'), 'feincms,medialibrary,south'),
    ('server_root_user', _(u'Name of server admin user?'), 'root'),
]

# make directory below workspace
# copy (or git clone) generic_django_project
# replace "project_name" in files...
# git init

# use feincms, medialibrary, photologue, daemontools, supervisord, celery, nginx/apache, mysql/postgresql ?

# get server name
# get server root account
# get server db root account
# make user account
# make db user account

answers = {}

widgets = [
]
offset = len(widgets) # number of widgets in front of questions
for key, text, default in questions:
    answers[key] = default
    widgets.append(urwid.Edit(('question', u'%s\n' % text), default))

content = urwid.SimpleListWalker(widgets)
listbox = urwid.ListBox(content)

def update(input):
    focus_widget, position = listbox.get_focus()
    if not hasattr(focus_widget, 'edit_text'):
        return
    if input == 'ctrl x': # delete input
        focus_widget.edit_text = ''
    if input in ('ctrl q', 'ctrl s', 'esc'):
        raise urwid.ExitMainLoop()
    key = questions[position-offset][0]
    answers[key] = focus_widget.edit_text
    listbox.set_focus(position+1)

header = urwid.Padding(urwid.Text(('header', _(u' Configure your project. Have fun! '))))
footer = urwid.Padding(urwid.Text(('footer', _(u' Abort with Ctrl-C, exit with Esc, delete a line with Ctrl-X. '))))

frame = urwid.Frame(listbox, header, footer)

loop = urwid.MainLoop(frame, palette, unhandled_input=update)
loop.run()

print answers
# STILL DOES NOTHING!
