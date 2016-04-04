#!/bin/bash
cd ~/workspace/project_name
for DIR in project_name other_app templates settings
do
  cd project_name/$DIR
  #if [ ! -d locale ]; then
  #  mkdir -pv locale/en/LC_MESSAGES
  #  mkdir -pv locale/de/LC_MESSAGES
  #fi
  django-admin makemessages -a -e .html,.py,.tex,.txt
  django-admin makemessages -a -e js -d djangojs
  open locale/*/LC_MESSAGES/*.po
  cd ../..
done
