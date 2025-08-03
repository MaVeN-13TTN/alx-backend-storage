#!/usr/bin/env python3
"""
Test file for task 1 - get methods
"""
Cache = __import__("exercise").Cache

cache = Cache()

TEST_CASES = {b"foo": None, 123: int, "bar": lambda d: d.decode("utf-8")}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    result = cache.get(key, fn=fn)
    print(f"Original: {value} ({type(value).__name__})")
    print(f"Key: {key}")
    print(f"Retrieved: {result} ({type(result).__name__})")
    print(f"Match: {result == value}")
    assert cache.get(key, fn=fn) == value
    print("✅ Test passed")
    print("---")

print("All tests passed!")
