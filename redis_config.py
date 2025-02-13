import os
import redis
from rq import Queue

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

q = Queue(connection=conn)

