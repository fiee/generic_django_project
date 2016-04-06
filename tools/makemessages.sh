#!/bin/bash
cd ~/workspace/project_name
for DIR in project_name other_app templates settings
do
  cd project_name/$DIR
  django-admin makemessages -a -e .html,.py,.tex,.txt
  django-admin makemessages -a -e js -d djangojs
  open locale/*/LC_MESSAGES/*.po
  cd ../..
done
