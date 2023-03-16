#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py djstripe_sync_models

gunicorn --bind 0.0.0.0:80 --workers 3 hackernews_developers.wsgi:application
