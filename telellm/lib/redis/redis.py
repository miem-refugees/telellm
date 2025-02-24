from redis import Redis

from telellm.lib.config.config import REDIS_HOST, REDIS_PORT


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
