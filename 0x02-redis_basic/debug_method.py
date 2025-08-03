#!/usr/bin/env python3
"""
Test to understand method structure for replay function
"""
Cache = __import__('exercise').Cache

cache = Cache()

# Store some data
cache.store("foo")
cache.store("bar")
cache.store(42)

# Check method attributes
print(f"Method: {cache.store}")
print(f"Method type: {type(cache.store)}")
print(f"Has __self__: {hasattr(cache.store, '__self__')}")
if hasattr(cache.store, '__self__'):
    print(f"__self__ type: {type(cache.store.__self__)}")
    print(f"Has _redis: {hasattr(cache.store.__self__, '_redis')}")

print(f"Method qualname: {cache.store.__qualname__}")
print(f"Method name: {cache.store.__name__}")
