======================
generic django project
======================

This is my starting point for a new Django_ site, mixed and stirred from several 
public sources and spiced with my own enhancements.

I normally work with FeinCMS_ and its medialibrary_, this is reflected in my setups.

My webserver of choice is Nginx_ with gunicorn_, since my virtual server is 
always low on memory.


------------
Requirements
------------

* server OS: Debian/Ubuntu based Linux
* local OS: MacOS X (only some local settings are OSX specific)
* web server: Nginx/gunicorn or Nginx/fcgi
* Python_ version: 2.7 or 3.x
* Django_ version: 1.9 (1.6+ should work)
* FeinCMS_ version: 1.5+
* version control: Git_
* deployment tool: Fabric_
* local development database: SQLite3_
* server database: MySQL_ or PostgreSQL_
* process control (optional): supervisord_ or daemontools_ 


---------
Rationale
---------

Django’s `startproject` doesn’t do enough. I’m a programmer, thus lazy, 
and try to reduce redundant work like repeating the same setup steps over and over. (DRY)

Just copying/cloning this generic project to a new site isn’t ideal either, 
since general changes don’t affect all dependent sites, but I got no idea how to do that.


------
Issues
------

I’m trying to keep this current and to implement what I learn from my actual 
projects and best practice advise. But since I mostly do other things than 
starting new django projects, I’m always far behind.

* While I try to adhere to best practices, there are probably security holes - 
  use at your own risk.
* Since I update this template after experiences with my actual sites,
  the commits are often not atomic.
* pip-installed requirements are not fixed on a version.
* I could also support runit_, but I didn't want to replace init.
* I’m not using daemontools_ any more, so its configuration is outdated.


-------
Details
-------

* gunicorn runs internally on an unix socket, because I find file locations 
  easier to control than server ports.
* I’m integrating Let’s Encrypt certificates and automating their renewal.
* My nginx settings get an A+ rating at SSLLabs_


-----
Ideas
-----

* Learn more from `Two Scoops of Django`_, http://djangopatterns.com and 
  https://github.com/callowayproject/django-app-skeleton
* Include Sphinx template
* Make ``django-admin.py startproject --template=https://github.com/fiee/generic_django_project/zipball/master --extension=py,rst,html,txt,ini,sh MY_PROJECT`` work
* Finally learn proper testing
* Split templates for simple site, cerebrale site, reusable app


-------
License
-------

This project template itself has no special license. Do with it what you want.
Attribution is appreciated. Corrections are welcome. I’m not responsible for
your failure, damage or loss.

Since it’s a collection of (modified) snippets from different sources that may
have different licenses, it would be impossible to untangle.

Following Django’s documentation I suggest to use a 2-clause BSD license for
your own projects.


------
How To
------

local:
------

* Copy ``generic_django_project``
* Rename "django_project" (this would be the project root as created by 
  ``django-admin.py startproject``)
* Replace all occurrences of lowercase "project_name" with your project name.
  This is also the webserver and database server username!
  The "project_name" directory is the one that would be created by
  ``manage.py startapp``.
* Check the settings in server-setup and django_project/settings:
  fabfile.py_, gunicorn-settings.py_,  supervisor.conf_,
  settings/base.py_, settings/local.py_ etc.
* Adapt LICENSE_ to your needs if you might publish your project.
  The 2-clause BSD license is just a suggestion.
* Set up an email account for your project’s error messages and configure it
  in settings/base.py_ and .env
* ``git init``, always commit all changes
* ``manage migrate`` (initialize migrations)
* ``fab webserver setup`` (once)
* ``fab webserver deploy`` (publish new release - always last committed version!)

Following 12-factor_ design, we now set our passwords and other secret settings 
as environment variables to avoid to have them in version control.
I suggest to go the *dotenv* route:

Put your settings into a ``.env`` file in the ``django_project`` directory,
to use with django-dotenv-rw_. Don’t forget to tell git to ignore .env files! ::

      DJANGO_SETTINGS_MODULE=settings
      DATABASE_PASSWORD=secret123
      EMAIL_PASSWORD=secret123

Alternatively add the settings to the end of your virtualenvs_ ``activate`` script: ::

      export DJANGO_SETTINGS_MODULE=settings
      export DATABASE_PASSWORD=secret123
      export EMAIL_PASSWORD=secret123


server:
-------

* Create the user

  I suggest to copy ``makeuser.sh``_ to your webserver’s root/admin account 
  and use it to create system and database accounts.
  
      scp makeuser.sh root@www.yourdomain.tld:/root/bin/
  
  Otherwise look into that script. This is just a part of the necessary setup:

  * create user and sudo-enable it (I suggest via a ``admin`` group, 
    but you can also add the user to ``sudoers``): ::

      adduser project_name --disabled-password --gecos ""
      adduser project_name admin

  * create database user and database (schema): ::
    
      mysql -u root -p
    
      # at first setup only: we installed MySQL without user interaction, 
      # so there’s no root password. Set it!
      use mysql;
      update user set password=password('...') where user='root';
    
      # create user and database for our project:
      create user 'project_name'@'localhost' identified by '...';
      create database project_name character set 'utf8';
      grant all privileges on project_name.* to 'project_name'@'localhost';
    
      flush privileges;
      quit;

* Create your ``.env`` file at ``/var/www/project_name`` 
  (or use virtualenvs_’ ``activate`` script), see above.

* Open your firewall for tcp 433 (not default on some systems).

* Request a SSL certificate, see e.g. https://www.nginx.com/blog/free-certificates-lets-encrypt-and-nginx/ ::

      sudo /opt/letsencrypt/letsencrypt-auto --config /etc/letsencrypt/configs/www.project_name.de.conf certonly


FeinCMS
-------

If you use FeinCMS’ Page, consider *first*, which extensions you’ll need – 
see the docs__ and the FAQ__ –
afterwards you would need to change the database table ``page_page`` by hand, 
since the changes aren’t always detected by migration!

.. __: http://www.feinheit.ch/media/labs/feincms/page.html#module-feincms.module.page.extension
.. __: http://www.feinheit.ch/media/labs/feincms/faq.html#i-run-syncdb-and-get-a-message-about-missing-columns-in-the-page-table

Have a look at Feinheit’s FeinCMS compatible apps, content types and plugins:
ElephantBlog_, form_designer_, feincms_gallery_ etc.

At the moment (April 2016) the released version of FeinCMS isn’t yet compatible
with Django 1.9; you must use the git checkout.


---------------
Links / Sources
---------------


Everything:
-----------

* `Two Scoops of Django`_


Setup:
------

* Nginx configuration: http://wiki.nginx.org/NginxConfiguration
* Secure Nginx TLS configuration: https://www.sherbers.de/howto/nginx/ (German)
* Gunicorn configuration: http://gunicorn.org/configure.html
* logrotate: e.g. http://www.linux-praxis.de/lpic1/manpages/logrotate.html
* daemontools: http://cr.yp.to/daemontools.html
* supervisord: http://supervisord.org
* Let’s Encrypt certificates with Nginx: https://www.nginx.com/blog/free-certificates-lets-encrypt-and-nginx/
* Let’s Encrypt certificates with Nginx: https://gist.github.com/xrstf/581981008b6be0d2224f


Modules:
--------

* Fabric: http://docs.fabfile.org
* MPTT: http://github.com/django-mptt/django-mptt
* FeinCMS: http://github.com/feincms/feincms
.. * Schedule: http://wiki.github.com/thauber/django-schedule/ or http://github.com/fiee/django-schedule

.. _Python: http://www.python.org
.. _Git: http://git-scm.com/
.. _Nginx: http://wiki.nginx.org
.. _Django: http://www.djangoproject.com/
.. _Fabric: http://docs.fabfile.org
.. _fabfile: http://docs.fabfile.org
.. _South: http://south.aeracode.org/
.. _MPTT: http://github.com/django-mptt/django-mptt
.. _FeinCMS: http://github.com/feincms/feincms
.. _medialibrary: http://www.feinheit.ch/media/labs/feincms/medialibrary.html
.. _ElephantBlog: https://github.com/feincms/feincms-elephantblog
.. _form_designer: https://github.com/feincms/form_designer
.. _feincms_gallery: https://github.com/feinheit/feincms_gallery
.. _Schedule: http://github.com/fiee/django-schedule
.. _gunicorn: http://gunicorn.org/
.. _mod_wsgi: http://modwsgi.readthedocs.org
.. _fcgi: http://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/
.. _MySQL: http://mysql.com/products/community/
.. _PostgreSQL: http://www.postgresql.org/
.. _SQLite3: http://www.sqlite.org/
.. _daemontools: http://cr.yp.to/daemontools.html
.. _supervisord: http://supervisord.org
.. _runit: http://smarden.org/runit/
.. _logrotate: http://www.linux-praxis.de/lpic1/manpages/logrotate.html
.. _virtualenvs: http://virtualenv.readthedocs.org/
.. _Redis: http://redis.io
.. _`Two Scoops of Django`: http://twoscoopspress.org/products/two-scoops-of-django-1-6
.. _django-dotenv-rw: http://github.com/tedtieken/django-dotenv-rw
.. _12-factor: http://12factor.net
.. _`maintenance page`: http://www.djangocurrent.com/2015/12/automatic-maintenance-page-for.html

.. _LICENSE: blob/master/reusable_app_project/LICENSE
.. _makeuser.sh: blob/master/tools/makeuser.sh
.. _manage.py: blob/master/django_project/manage.py
.. _settings/base.py: blob/master/django_project/project_name/settings/base.py
.. _settings/local.py: blob/master/django_project/project_name/settings/local.py
.. _gunicorn-settings.py: blob/master/deploy/gunicorn-settings.py
.. _fabfile.py: blob/master/fabfile.py
.. _supervisor.ini: blob/master/deploy/supervisor.ini
.. _service-run.sh: blob/master/deploy/service-run.sh
.. _nginx.conf: blob/master/deploy/nginx.conf

.. _SSLLabs: https://www.ssllabs.com/ssltest/

