#!/usr/bin/env python3
"""
Web caching module with Redis.

This module implements a web cache with expiration and request tracking
using Redis for storage.
"""

import redis
import requests
import functools
from typing import Callable, Optional, Union, cast


# Global Redis instance
_redis = redis.Redis()


def cache_with_expiration(expiration: int = 10):
    """
    Decorator to cache function results with expiration time.

    Args:
        expiration: Cache expiration time in seconds (default: 10)

    Returns:
        Decorated function with caching capability
    """

    def decorator(method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(url: str) -> str:
            # Create cache key
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Try to get from cache first
            cached_result = _redis.get(cache_key)
            if cached_result is not None:
                # Increment access counter and set expiration to match cache
                _redis.incr(count_key)
                _redis.expire(count_key, expiration)
                # Type cast to bytes before decode since Redis returns bytes
                return cast(bytes, cached_result).decode("utf-8")

            # If not in cache, call the original function
            result = method(url)

            # Store in cache with expiration
            _redis.setex(cache_key, expiration, result)

            # Increment access counter and set same expiration
            _redis.incr(count_key)
            _redis.expire(count_key, expiration)

            return result

        return wrapper

    return decorator


@cache_with_expiration(10)
def get_page(url: str) -> str:
    """
    Fetch HTML content from a URL with caching and tracking.

    This function:
    - Tracks how many times a URL was accessed in "count:{url}"
    - Caches the result with 10 seconds expiration time
    - Returns the HTML content of the URL

    Args:
        url: The URL to fetch

    Returns:
        HTML content as string
    """
    response = requests.get(url)
    return response.text


def get_access_count(url: str) -> int:
    """
    Get the number of times a URL was accessed.

    Args:
        url: The URL to check

    Returns:
        Number of times the URL was accessed
    """
    count = _redis.get(f"count:{url}")
    return int(cast(bytes, count).decode("utf-8")) if count is not None else 0


# Alternative implementation without decorator (if needed)
def get_page_simple(url: str) -> str:
    """
    Simple implementation without decorator for comparison.

    Args:
        url: The URL to fetch

    Returns:
        HTML content as string
    """
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"

    # Try to get from cache first
    cached_result = _redis.get(cache_key)
    if cached_result is not None:
        # Increment access counter and set expiration to match cache
        _redis.incr(count_key)
        _redis.expire(count_key, 10)
        return cast(bytes, cached_result).decode("utf-8")

    # If not in cache, fetch from URL
    response = requests.get(url)
    result = response.text

    # Store in cache with 10 seconds expiration
    _redis.setex(cache_key, 10, result)

    # Increment access counter and set same expiration
    _redis.incr(count_key)
    _redis.expire(count_key, 10)

    return result
