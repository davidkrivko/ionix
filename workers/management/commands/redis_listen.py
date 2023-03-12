from django.core.management.base import BaseCommand
import os
import logging
import redis

from ioniqbox.settings import REDIS_LOCATION_STRING
from workers.tasks import trigger_warm_weather_shutdown_check


class Command(BaseCommand):
    help = 'Listens to Redis channel and triggers function when message is received'

    def handle(self, *args, **options):
        trigger_warm_weather_shutdown_check()
