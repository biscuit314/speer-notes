import logging
import redis

from configuration import SETTINGS

LOG = logging.getLogger('redis')

SETTINGS.set_prefix_description('REDIS', 'Connection details to the Redis server')
SETTINGS.create('REDIS', {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0
})


def get_redis_client():
    return redis.Redis(
        host=SETTINGS.get('REDIS_HOST', 'localhost'),
        port=SETTINGS.get('REDIS_PORT', 6379),
        db=SETTINGS.get('REDIS_DB', 0)
    )
