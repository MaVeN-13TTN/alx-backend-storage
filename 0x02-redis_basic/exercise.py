#!/usr/bin/env python3
"""
Redis Cache class module.

This module contains a Cache class that provides basic Redis operations
for storing and retrieving data with random keys.
"""

import redis
import uuid
import functools
from typing import Union, Callable, Optional, Any


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The wrapped method that stores call history in Redis.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output history.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The return value of the original method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the original method
        output = method(self, *args, **kwargs)

        # Store output
        self._redis.rpush(output_key, output)

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The wrapped method that increments a counter in Redis.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the method call count.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The return value of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


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

    @call_history
    @count_calls
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


def replay(method) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        method: The bound method to display call history for.
    """
    # Get the Redis instance from the method's bound instance
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    # Get the call count
    count = redis_instance.get(method_name)
    if count is None:
        count = 0
    else:
        count = int(count)

    print(f"{method_name} was called {count} times:")

    # Get input and output history
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    # Display each call
    for inp, out in zip(inputs, outputs):
        input_str = inp.decode('utf-8')
        output_str = out.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")
