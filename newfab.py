#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Building site for a new deployment toolset

ATM mostly shell commands
"""

@task
def setup(c):
    pass
    adduser "USER" --disabled-password --gecos ""
    mkdir /var/www/USER/{run,log,backup,letsencrypt}
    cd /var/www/USER
    virtualenv .
    # .env
    # MySQL-User
    mkdir /var/tmp/django_cache/USER
    cd ~
    ln -s /var/www/USER www
    echo "\ncd /var/www/USER && source bin/activate\n" >> ~/.profile
    cd .ssh


@task
def install(c):
    pass
    cd /var/www/USER
    git clone git@git.fiee.net:USER.git
    update()
    chmod go+w /var/www/USER/log/*.log
    supervisorctl update
    service nginx reload
    certbot certonly --nginx


@task
def update(c):
    pass
    cd /var/www/USER/USER
    git pull
    rm USER/settings/local.*
    pip3 install -U -r requirements/webserver.txt
    cd USER
    python manage.py migrate
    python manage.py collectstatic
    cd ..
    cp server-setup/nginx.conf /etc/nginx/sites-available/USER.conf
    cp server-setup/supervisor.conf /etc/supervisor/conf.d/USER.conf
