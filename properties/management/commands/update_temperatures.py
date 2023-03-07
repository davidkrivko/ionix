from django.core.management.base import BaseCommand
from properties.models import ZipCodeModel
import requests


class Command(BaseCommand):
    help = 'Update temperatures for all ZIP codes'

    def handle(self, *args, **options):
        for zip_code in ZipCodeModel.objects.all():
            url = f'https://api.openweathermap.org/data/2.5/weather?zip=' \
                  f'{zip_code.zip_code}&appid=6bbeb61dded83964d1903f45590a4335&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                zip_code.todays_temp = temperature
                zip_code.save()


comm = Command()

print(comm.handle())
