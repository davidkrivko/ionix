import redis

r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()


def myfunction():
    print("Running myfunction")


p.subscribe('mychannel')

for message in p.listen():
    if message['data'] == b'run myfunction':
        myfunction()
