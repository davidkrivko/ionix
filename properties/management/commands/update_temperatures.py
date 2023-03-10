from django.core.management.base import BaseCommand
from properties.models import ZipCodeModel
import requests


class Command(BaseCommand):
    help = 'Update temperatures for all ZIP codes'

    def handle(self, *args, **options):
        for zip_code in ZipCodeModel.objects.all():
            url = f'https://api.openweathermap.org/data/2.5/' \
                  f'weather?zip={zip_code.zip_code}&appid=4c1' \
                  f'782a65f1e266cace6cd370f9da9bb&units=imperial'
            response = requests.get(url)
            try:
                data = response.json()
                temperature = int(data['main']['temp'])
                zip_code.todays_temp = temperature
                zip_code.save()
            except:
                continue


comm = Command()

print(comm.handle())
