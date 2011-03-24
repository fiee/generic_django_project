======================
generic django project
======================

This is my starting point for a new Django_ site, mixed and stirred from several public sources and spiced with my own enhancements.

I normally work with FeinCMS_ and its medialibrary_, but sometimes also with Photologue_ and Schedule_, this is reflected in my setups.

My webserver of choice is Nginx_ with gunicorn_, since my virtual server is always low on memory. Setup for Apache_ with mod_wsgi_ and Nginx_ with fcgi_ is also provided.


------------
Requirements
------------

* server OS: Debian/Ubuntu based Linux
* local OS: MacOS X (only some local settings are OSX specific)
* web server: Apache/mod_wsgi or Nginx/gunicorn or Nginx/fcgi
* Python_ version: 2.5+
* Django_ version: 1.3
* version control: Git_
* deployment tool: Fabric_
* local development database: SQLite3_
* server database: MySQL_ or PostgreSQL_
* database migration: South_
* process control (optional): daemontools_ or supervisord_


---------
Rationale
---------

Django's startproject doesn't do enough. I'm a programmer, thus lazy, and try to reduce redundant work like repeating the same setup steps over and over. (DRY)

Just copying this generic project to a new site isn't ideal either, since general changes don't affect all dependent sites, but I got no idea how to do that.


------
Issues
------

* User creation isn't integrated in fabfile_ setup.
* Probably security holes - use at your own risk.
* I could also support runit_, but I didn't want to replace init
* South_ still doesn't work for me, must overcome problems with several releases and multiple projects accessing the same Django_ app outside of virtualenvs_


------
How To
------

local:
------

* copy `generic_project`
* replace all occurrences of lowercase "project_name" with your project name. this is also the webserver and database server username!
* check the settings in fabfile.py_, gunicorn-settings.py_, settings.py_, settings_local.py_, supervisor.ini_ or service-run.sh_
* set up an email account for your project’s error messages and configure it in settings.py_
* if you use Nginx, change the internal port in nginx.conf_ (``fastcgi_pass 127.0.0.1:8001;``); I use "8 + last 3 numbers of UID" (UIDs start at 1000 on Debian): ``id -u project_name``
* ``git init``, always commit all changes
* ``manage syncdb`` (initialize south)
* ``fab webserver setup`` (once)
* ``fab webserver deploy`` (publish new release - always last committed version!)

server:
-------

I suggest to use makeuser.sh_ to create system and database accounts. Otherwise:

* create user and sudo-enable it (I suggest via a group like wheel, but you can also add the user to sudoers)::
  
    adduser project_name
    adduser project_name wheel

* create database user and database (schema) ::
  
    mysql -u root -p
    
    # at first setup only: we installed MySQL without user interaction, so there's no root password. Set it!
    use mysql;
    update user set password=password('...') where user='root';
  
    # create user and database for our project:
    create user 'project_name'@'localhost' identified by '...';
    create database project_name character set 'utf8';
    grant all privileges on project_name.* to 'project_name'@'localhost';
  
    flush privileges;
    quit;


FeinCMS
-------

If you use FeinCMS’ Page, consider *first*, which extensions you’ll need - 
see the docs__ and the FAQ__ -
afterwards you would need to change the database table `page_page` by hand, 
since the changes aren’t detected by South!

.. __: http://www.feinheit.ch/media/labs/feincms/page.html#module-feincms.module.page.extension
.. __: http://www.feinheit.ch/media/labs/feincms/faq.html#i-run-syncdb-and-get-a-message-about-missing-columns-in-the-page-table


---------------
Links / Sources
---------------

Setup:
------

* Setup with Apache/mod_wsgi: http://morethanseven.net/2009/07/27/fabric-django-git-apache-mod_wsgi-virtualenv-and-p/
* Setup with Nginx: http://djangoadvent.com/1.2/deploying-django-site-using-fastcgi/
* Nginx configuration: http://wiki.nginx.org/NginxConfiguration
* Gunicorn configuration: http://gunicorn.org/configure.html
* logrotate: e.g. http://www.linux-praxis.de/lpic1/manpages/logrotate.html
* daemontools: http://cr.yp.to/daemontools.html
* supervisord: http://supervisord.org

Modules:
--------

* Fabric: http://docs.fabfile.org
* South: http://south.aeracode.org/ (Getting started: http://mitchfournier.com/?p=25)
* MPTT: http://code.google.com/p/django-mptt/ or http://github.com/django-mptt/django-mptt
* FeinCMS: http://github.com/matthiask/feincms
* Schedule: http://wiki.github.com/thauber/django-schedule/ or http://github.com/fiee/django-schedule

.. _Python: http://www.python.org
.. _Git: http://git-scm.com/
.. _Nginx: http://wiki.nginx.org
.. _Django: http://www.djangoproject.com/
.. _Fabric: http://docs.fabfile.org
.. _fabfile: http://docs.fabfile.org
.. _South: http://south.aeracode.org/
.. _MPTT: http://github.com/django-mptt/django-mptt
.. _FeinCMS: http://github.com/matthiask/feincms
.. _medialibrary: http://www.feinheit.ch/media/labs/feincms/medialibrary.html
.. _Photologue: http://code.google.com/p/django-photologue/
.. _Schedule: http://github.com/fiee/django-schedule
.. _gunicorn: http://gunicorn.org/
.. _Apache: http://httpd.apache.org/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _fcgi: http://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/
.. _MySQL: http://mysql.com/products/community/
.. _PostgreSQL: http://www.postgresql.org/
.. _SQLite3: http://www.sqlite.org/
.. _daemontools: http://cr.yp.to/daemontools.html
.. _supervisord: http://supervisord.org
.. _runit: http://smarden.org/runit/
.. _logrotate: http://www.linux-praxis.de/lpic1/manpages/logrotate.html
.. _virtualenvs: http://virtualenv.readthedocs.org/

.. _makeuser.sh: blob/master/tools/makeuser.sh
.. _settings.py: blob/master/project_name/settings.py
.. _settings_local.py: blob/master/project_name/settings_local.py
.. _gunicorn-settings.py: blob/master/gunicorn-settings.py
.. _fabfile.py: blob/master/fabfile.py
.. _supervisor.ini: blob/master/supervisor.ini
.. _service-run.sh: blob/master/service-run.sh
.. _nginx.conf: blob/master/nginx.conf
