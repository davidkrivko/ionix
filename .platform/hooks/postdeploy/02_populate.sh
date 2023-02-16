#!/bin/bash

source /var/app/venv/*/bin/activate && {
# populate schedule options
python manage.py populate_schedule;
}