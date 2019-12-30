====================
reusable_app_project
====================

This is the start for your own documentation.


------------
Requirements
------------

* Python_ 3.7+
* Django_ 3.0+


------
Issues
------

* No known issues yet


-----------
Quick start
-----------

1. Add `project_name` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = [
        ...
        'project_name',
    ]

2. Include the project_name URLconf in your project `urls.py` like this::

    url(r'^project_name/', include('project_name.urls')),

3. Run `python manage.py migrate` to create the project_name models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create project_name objects (you’ll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/project_name/


-------
License
-------

Two-clause BSD, see LICENSE_


-------
Authors
-------

* You <you@yourdomain.com>


.. _Python: http://www.python.org
.. _Git: http://git-scm.com/
.. _Nginx: http://wiki.nginx.org
.. _Django: http://www.djangoproject.com/

.. _LICENSE: blob/master/reusable_app_project/LICENSE
