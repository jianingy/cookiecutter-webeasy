# -*- coding: UTF-8 -*-
from gevent import socket as gsocket
import redis
import redis.connection

from .exceptions import ServerException

redis.connection.socket = gsocket


class RedisFactoryError(ServerException):
    error_code = 500002


class RedisFactory:
    _pools = {}

    def __init__(self):
        raise RuntimeError('cannot initialize an instance of this class')

    @classmethod
    def connect(cls, uri, name='default'):
        if name not in cls._pools:
            cls._pools[name] = redis.ConnectionPool.from_url(uri)
        return redis.StrictRedis(connection_pool=cls._pools[name])

    @classmethod
    def create(cls, name='default'):
        if name not in cls._pools:
            raise RedisFactoryError(reason='redis connection not connected')
        return redis.StrictRedis(connection_pool=cls._pools[name])

    @classmethod
    def get_connection_pool(cls, name='default'):
        if name not in cls._pools:
            raise RedisFactoryError(reason='redis connection not connected')
        return cls._pools[name]
