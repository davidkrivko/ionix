import re
import requests
import logging

from django.utils import timezone

from properties.models import (
    ZipCodeModel,
    WeatherRecordModel,
)
from django_q.tasks import async_task, async_iter
from devices.utils import insert_weather_data
from dateutil.relativedelta import relativedelta


def parse_temp_from_weathergov(zip_pk: int):
    """
    Extracts lat and lon records from the
    ZipCode model and saves last observ. temp in it.

    Args:
        zip_pk (int): ZipCode model pk
    """

    zip_obj = ZipCodeModel.objects.get(pk=zip_pk)

    lat = zip_obj.lat_coord
    lon = zip_obj.lon_coord

    if lat is None and lon is None:
        logging.warning("Lat and Lon coord-s are not set")
        return

    headers = {
            f"User-Agent": "Ioniqbox <alert@ioniqbox.com>"
        }

    GRID_POINTS_LINK = f"https://api.weather.gov/points/{lat},{lon}"

    grid_response = requests.get(GRID_POINTS_LINK, headers=headers)

    stations_endpoint = None
    if grid_response.status_code == 200:
        stations_endpoint = grid_response.json()['properties']['observationStations']

    station = None
    temperature_f = None

    if stations_endpoint is not None:

        stations_list_response = requests.get(stations_endpoint)

        if stations_list_response.status_code == 200:
            station = stations_list_response.json()['observationStations'][0]

    if station is not None:
        observations_endpoint = station + '/observations/latest/'
        observations_response = requests.get(observations_endpoint)

        if observations_response.status_code == 200:

            temperature_c = observations_response.json()['properties']['temperature']['value']

            temperature_f = None
            if temperature_c is not None:
                temperature_f = (temperature_c * 9/5) + 32
            
                zip_obj.todays_temp = temperature_f
                zip_obj.updated_at = timezone.now()
                zip_obj.save()

                # async_task('devices.utils.insert_weather_data', zip_obj.zip_code, temperature_f, temperature_c)

                WeatherRecordModel.objects.create(
                    zip_code=zip_obj,
                    temp_f=temperature_f,
                    temp_c=temperature_c,
                )

    return f"Temp F {temperature_f}"


def migrate_temp_records():
    """
    One-time handler to move existing records
    from Django to remote cold db
    """
    print("WeatherRecordModel.objects.all()", WeatherRecordModel.objects.all())
    iter = [obj.pk for obj in WeatherRecordModel.objects.all()]
    print("iter", iter)
    async_iter('api.utils.migrate_temp_record', iter)


def migrate_temp_record(record_pk: int):
    """
    Custom function to export record to remote postgres
    """

    record = WeatherRecordModel.objects.get(pk=record_pk)
    # print("record", record)
    zip_code = record.zip_code.zip_code
    # print("zip_code", zip_code)
    temp_c = record.temp_c
    # print("temp_c", temp_c)
    temp_f = record.temp_f
    real_time = record.created_at
    # print("real_time", real_time)

    insert_weather_data(zip_code, temp_f, temp_c, real_time=real_time)
