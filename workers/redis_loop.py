import os
import logging
import redis


from workers.tasks import trigger_warm_weather_shutdown_check


logger = logging.getLogger('django')
logger.setLevel(logging.INFO)


r = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=int(os.environ.get("REDIS_PORT")),
    db=1,
    username=os.environ.get("REDIS_NAME"),
    password=os.environ.get("REDIS_PASSWORD")
)
p = r.pubsub()

p.subscribe('mychannel')
logger.info("We are in redis_loop")

for message in p.listen():
    if message['data'] == b'run myfunction':
        trigger_warm_weather_shutdown_check()
