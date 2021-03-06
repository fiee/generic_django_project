======================
generic django project
======================

This is my starting point for a new Django_ site, mixed and stirred
from several public sources and spiced with my own enhancements.

I usually work with FeinCMS_ and its medialibrary_, this is reflected
in my setups.

My webserver of choice is Nginx_ with gunicorn_.


------------
Requirements
------------

* server OS: Debian/Ubuntu based Linux
* local OS: macOS (only some local settings are OSX specific)
* web server: Nginx/gunicorn
* Python_ version: 3.6+
* Django_ version: 2.2
* FeinCMS_ version: 1.17+
* version control: Git_ (with a remote git host)
* deployment tool: Fabric_
* local development database: SQLite3_ or MariaDb/MySQL_
* server database: MariaDb/MySQL_
* process control (optional): supervisord_


---------
Rationale
---------

I don’t know if this still makes sense, but while I update some sites
from Django 1.9 to 3.0 I also update this.

Django’s `startproject` doesn’t do enough. I’m a programmer, thus lazy,
and try to reduce redundant work like repeating the same setup steps over and over. (DRY)

Just copying/cloning this generic project to a new site isn’t ideal either,
since general changes don’t affect all dependent sites, but I got no idea
how to do that.


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
* I handle migrations wrongly, will try to fix soon.
* pip-installed requirements are not fixed on a version.
* I could also support runit_, but I didn't want to replace init.
* PostgreSQL would make sense, but I don’t need it.


-------
Details
-------

* gunicorn runs internally on an unix socket, because I find file locations
  easier to control than server ports.
* My earlier Fabric workflow used only local git and pushed a package to the
  web server. Now I’m relying on my private git server (gitolite) and doing
  away with different releases on the web server. This might also fit some
  shared hosting providers with git-enabled Plesk.
* I’m using Let’s Encrypt certificates with certbot.
* My nginx settings get an A+ rating at SSLLabs_ (still?)


-----
Ideas
-----

* Learn more from e.g. `Two Scoops of Django`_, http://agiliq.com/books/djangodesignpatterns/,
  https://github.com/callowayproject/django-app-skeleton,
  https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
* Include Sphinx template
* Make ``django-admin.py startproject --template=https://github.com/fiee/generic_django_project/zipball/master --extension=py,rst,html,txt,ini,sh MY_PROJECT`` work
* Maybe use cookiecutter. Investigate other deployment tools.
* Finally learn proper testing
* Split templates for simple site, celery site, reusable app
* Change workflow from local git plus website releases to local+remote git
* Add setup for Wagtail (and Longclaw)


-------
License
-------

This project template itself has no special license. Do with it what you want.
Attribution is appreciated. Corrections are welcome. I’m not responsible for
your failure, damage or loss.

Since it’s a collection of (modified) snippets from different sources that may
have different licenses, it would be impossible to untangle.

Following Django’s documentation I suggest to use a 2-clause BSD license for
your own reusable projects.


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
* cd into your project directory, ``virtualenv .``
  (create virtual environment; make sure you use the right version)
* ``. bin/activate`` (activate virtual environment)
* ``bin/pip install -r requirements/local.txt`` (install requirements)
* ``cd <project_name>``
* ``vi .env`` (create .env file, see below)
* ``./manage.py migrate`` (initialize migrations)
* ``git init``, always commit all changes
* ``fab webserver setup`` (once)
* ``fab webserver deploy`` (publish new release - always last committed version!)

Following 12-factor_ design, we now set our passwords and other secret settings
as environment variables to avoid to have them in version control.
I suggest to go the *dotenv* route:

Put your settings into a ``.env`` file in the ``django_project`` directory,
to use with django-dotenv_. Don’t forget to tell git to ignore .env files! ::

      DJANGO_SETTINGS_MODULE=settings
      SECRET_KEY=secret123
      DATABASE_PASSWORD=secret123
      EMAIL_PASSWORD=secret123

Alternatively add the settings to the end of your virtualenvs_ ``activate`` script: ::

      export DJANGO_SETTINGS_MODULE=settings
      export SECRET_KEY=secret123
      export DATABASE_PASSWORD=secret123
      export EMAIL_PASSWORD=secret123


server:
-------

* Create the user

  I suggest to copy makeuser.sh_ to your webserver’s root/admin account
  and use it to create system and database accounts.

      scp makeuser.sh root@www.yourdomain.tld:/root/bin/

  Otherwise look into that script. This is just a part of the necessary setup:

  * create user and sudo-enable it (I suggest via a ``admin`` group,
    but you can also add the user to ``sudoers``): ::

      adduser project_name --disabled-password --gecos ""
      adduser project_name admin

    REM: It’s possible to avoid sudo rights for each website user, but
    then you need to run some commands as root or as an other sudo-enabled user.

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

* publish your project (``fab webserver setup``)

* Open your firewall for tcp 433 (not default on some systems).

* Create a ssh key for the new user: ::

    ssh-keygen -b 4096

* Add this key to your git server’s access configuration, e.g. like ::

    scp project_name@webserver.tld:/home/project_name/.ssh/id_rsa.pub gitolite-admin/keydir/project_name@webserver.pub

  You need read access for ``project_name`` on the web server
  and write access for your development user.

* Publish your project to your git server and
  clone the project on your web server, e.g. as
  ``/var/www/project_name/project_name``.

* Activate the project in supervisor.

* Run certbot to acquire a SSL certificate for your project.

* (This is WIP)

FeinCMS
-------

If you use FeinCMS’ Page, consider *first*, which extensions you’ll need –
see `the docs <http://feincms-django-cms.readthedocs.io/en/latest/page.html#module-feincms.module.page.extension>`_ – the migration is somewhat tricky.

Since the setup requires monkey patching FeinCMS’s models, you must pull their
migrations into your app, as outlined in `the docs <http://feincms-django-cms.readthedocs.io/en/latest/migrations.html>`_.
The same is true for Plata_.

Have a look at Feinheit’s FeinCMS compatible apps, content types and plugins:
ElephantBlog_, Plata_, form_designer_ etc. (REM: They’re mostly outdated.)

Instead of FeinCMS’s medialibrary, consider to use django-filer_ instead,
there’s some support for it in FeinCMS, but not yet here.


---------------
Links / Sources
---------------


Everything:
-----------

* `Two Scoops of Django`_


Setup:
------

* Nginx configuration: http://wiki.nginx.org/NginxConfiguration
* Secure Nginx configuration: https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html
  or https://www.sherbers.de/howto/nginx/ (German)
* Gunicorn configuration: http://gunicorn.org/configure.html
* logrotate: e.g. http://www.linux-praxis.de/lpic1/manpages/logrotate.html
* supervisord: http://supervisord.org


Modules:
--------

* Fabric: http://docs.fabfile.org
* MPTT: http://github.com/django-mptt/django-mptt
* FeinCMS: http://github.com/feincms/feincms

.. _Python: http://www.python.org
.. _Git: http://git-scm.com/
.. _Nginx: http://wiki.nginx.org
.. _Django: http://www.djangoproject.com/
.. _Fabric: http://docs.fabfile.org
.. _fabfile: http://docs.fabfile.org
.. _django-filer: https://django-filer.readthedocs.io
.. _MPTT: http://github.com/django-mptt/django-mptt
.. _FeinCMS: http://github.com/feincms/feincms
.. _medialibrary: http://feincms-django-cms.readthedocs.io/en/latest/medialibrary.html
.. _Plata: https://github.com/fiee/plata
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
.. _django-dotenv: https://pypi.python.org/pypi/django-dotenv/
.. _12-factor: http://12factor.net
.. _`maintenance page`: http://www.djangocurrent.com/2015/12/automatic-maintenance-page-for.html

.. _LICENSE: blob/master/reusable_app_project/LICENSE
.. _makeuser.sh: blob/master/tools/makeuser.sh
.. _manage.py: blob/master/django_project/manage.py
.. _base.py: blob/master/django_project/project_name/settings/base.py
.. _local.py: blob/master/django_project/project_name/settings/local.py
.. _gunicorn-settings.py: blob/master/server-setup/gunicorn-settings.py
.. _fabfile.py: blob/master/fabfile.py
.. _supervisor.conf: blob/master/server-setup/supervisor.ini
.. _service-run.sh: blob/master/server-setup/service-run.sh
.. _nginx.conf: blob/master/server-setup/nginx.conf

.. _SSLLabs: https://www.ssllabs.com/ssltest/

