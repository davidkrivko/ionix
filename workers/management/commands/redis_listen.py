from django.core.management.base import BaseCommand
import os
import logging
import redis

from ioniqbox.settings import REDIS_LOCATION_STRING
from workers.tasks import trigger_warm_weather_shutdown_check


class Command(BaseCommand):
    help = 'Listens to Redis channel and triggers function when message is received'

    def handle(self, *args, **options):
        logger = logging.getLogger('django')
        logger.setLevel(logging.INFO)

        r = redis.Redis.from_url(REDIS_LOCATION_STRING)
        p = r.pubsub()

        p.subscribe('mychannel')
        logger.info("We are in redis_loop")

        for message in p.listen():
            if message['data'] == b'run myfunction':
                trigger_warm_weather_shutdown_check()
