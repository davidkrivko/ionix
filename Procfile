web: gunicorn --bind :8000 --workers 3 --threads 2 ioniqbox.wsgi:application
worker: python manage.py qcluster --settings=ioniqbox.settings