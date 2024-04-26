#!/bin/sh

set -e

python manage.py wait_for_db
# Django static files will be served by Nginx
python manage.py collectstatic --noinput
python manage.py migrate

# Start uWSGI
# --socket :9000: uWSGI will listen on port 9000
# --workers 4: 4 worker processes will be spawned
# --master: master process will be started
# --enable-threads: enable threading
# --module app.wsgi: the WSGI module to use (app/app/wsgi.py)
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi