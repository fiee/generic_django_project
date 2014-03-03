#!/usr/bin/env bash
# service runner for daemontools
SITE=project_name
SITEUSER=$SITE

SITEDIR=/var/www/${SITE}
DJANGODIR=${SITEDIR}/releases/current/${SITE}
PYTHON=${SITEDIR}/bin/python
CELERYLOG="--logfile=${SITEDIR}/logs/celery.log"

# activate virtualenv
source ${SITEDIR}/bin/activate
cd ${SITEDIR}
# run celery daemon
# --beat --events
#exec envuidgid $SITEUSER $PYTHON $DJANGODIR/manage.py celeryd -E $CELERYLOG 
exec setuidgid $SITEUSER $PYTHON $DJANGODIR/manage.py celeryd -E $CELERYLOG 
