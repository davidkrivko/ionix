#!/bin/bash

source /var/app/venv/*/bin/activate && {

# collect static
python manage.py collectstatic --noinput;
# log which migrations have already been applied
python manage.py showmigrations;
# migrate the rest
python manage.py migrate --noinput;
python manage.py migrate sessions --noinput;
# create superuser
python manage.py createsu;
}