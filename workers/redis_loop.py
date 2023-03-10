import redis

from workers.tasks import trigger_warm_weather_shutdown_check

r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()


p.subscribe('mychannel')

for message in p.listen():
    if message['data'] == b'run myfunction':
        trigger_warm_weather_shutdown_check()
