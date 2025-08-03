#!/usr/bin/env python3
"""
Redis Cache class module.

This module contains a Cache class that provides basic Redis operations
for storing and retrieving data with random keys.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for Redis operations.

    This class provides methods to store data in Redis using random keys
    and retrieve the data later.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance.

        Creates a Redis client instance and flushes the database to start
        with a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.

        Args:
            data: The data to store. Can be str, bytes, int, or float.

        Returns:
            str: The random key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
