from . import *


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
        'ROUTING': 'talkyo.routing.channel_routing',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
        'PASSWORD': 'postgres',
        'PORT': 5432,
    }
}

LANGUAGE_MODEL = 'en_vectors_web_lg'
