# IONIQBOX PROJECT V2

## Running locally

Use poetry to install dependencies:

`pipenv shell`
`pipenv install`

Activate environment:

`pipenv shell`

````shell
    python -m venv venv
    venv\Scriprts\activate.bat
    pip install pipenv
    pipenv lock -r > requirements.txt
    pip install -r requirements.txt
````

## .env file

Use should connect env file to your interpreter and run it with it

````shell
DJANGO_ADMIN_PASS=Gbk6ciPUDI
DJANGO_SECRET_KEY=6y78QJONkVXgy3U7i6mhJdz6fqxymqni
DJANGO_SETTINGS_MODULE=ioniqbox.settings
EMAIL_HOST_PASSWORD=maksym_shemet
EMAIL_HOST_USER=alert@ioniqbox.com
RDS_DB_NAME=NAME
RDS_HOSTNAME=HOST
RDS_PASSWORD=PASSWORD
RDS_PORT=PORT
RDS_USERNAME=USERNAME
SERVICE_TOKEN=3ODhO9ak730ap4jfkGAQ6m25U4xNDxgW
THERMOSTAT_TOKEN=n@~)Ku`?^G76iG9
REDIS_HOST=HOST
REDIS_PORT=PORT
REDIS_PASSWORD=PASSWORD
REDIS_NAME=NAME
````


Run Django

`./manage.py runserver`

Staging env: panels-staging.turnonheat.com
             ioadmin-staging.turnonheat.com