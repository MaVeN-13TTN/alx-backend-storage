#!/usr/bin/env python3
"""
Test file for count_calls decorator
"""
Cache = __import__("exercise").Cache

print("=== Testing count_calls decorator ===")

cache = Cache()

# Test that the store method is decorated
print(f"Store method qualname: {cache.store.__qualname__}")

# Test initial count (should be 0)
initial_count = cache.get(cache.store.__qualname__)
print(f"Initial count: {initial_count}")

# Store some data and check count increments
print("\nStoring data and checking counts:")
for i in range(5):
    data = f"test_data_{i}".encode()
    key = cache.store(data)
    count = cache.get(cache.store.__qualname__)
    print(f"After store #{i+1}: count = {count}")

# Verify the decorator preserves the original function
print(f"\nOriginal function name preserved: {cache.store.__name__}")
print(f"Original function docstring exists: {cache.store.__doc__ is not None}")

# Test that other methods are not counted
print(f"\nCalling get method (should not affect store count):")
result = cache.get(cache.store.__qualname__)
count_after_get = cache.get(cache.store.__qualname__)
print(f"Count after get call: {count_after_get} (should be same as before)")

print("\n✅ All tests completed!")
