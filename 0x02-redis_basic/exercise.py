#!/usr/bin/env python3
"""
Redis Cache class module.

This module contains a Cache class that provides basic Redis operations
for storing and retrieving data with random keys.
"""

import redis
import uuid
from typing import Union, Callable, Optional, Any


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

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Get data from Redis and optionally apply a conversion function.

        Args:
            key: The key to retrieve data for.
            fn: Optional callable to convert the data back to desired format.

        Returns:
            The data from Redis, optionally converted, or None if key
            doesn't exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Get data from Redis and convert it to a string.

        Args:
            key: The key to retrieve data for.

        Returns:
            The data as a string, or None if key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Get data from Redis and convert it to an integer.

        Args:
            key: The key to retrieve data for.

        Returns:
            The data as an integer, or None if key doesn't exist.
        """
        return self.get(key, fn=int)
