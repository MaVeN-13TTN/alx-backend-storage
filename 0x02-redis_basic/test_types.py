#!/usr/bin/env python3
"""
Test file to verify different data types
"""
import redis

Cache = __import__("exercise").Cache

cache = Cache()

# Test with different data types
test_data = [b"hello", "world", 42, 3.14]  # bytes  # string  # int  # float

local_redis = redis.Redis()

for data in test_data:
    key = cache.store(data)
    stored_value = local_redis.get(key)
    print(f"Original: {data} (type: {type(data).__name__})")
    print(f"Key: {key}")
    print(f"Stored: {stored_value} (type: {type(stored_value).__name__})")
    print("---")
