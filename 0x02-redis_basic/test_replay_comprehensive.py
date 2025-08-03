#!/usr/bin/env python3
"""
Comprehensive test for replay function
"""
from exercise import Cache, replay

print("=== Testing replay function ===")

cache = Cache()

# Test with no calls first
print("1. Testing with no calls:")
replay(cache.store)

print("\n2. Testing with various data types:")
cache.store("first string")
cache.store(42)
cache.store(3.14)
cache.store(b"bytes data")

replay(cache.store)

# Test that replay works after more calls
print("\n3. Testing after additional calls:")
cache.store("additional")
replay(cache.store)

print("\n✅ All replay tests completed!")
