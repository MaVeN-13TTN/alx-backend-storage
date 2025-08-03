#!/usr/bin/env python3
"""
Test decorator behavior with multiple instances
"""
Cache = __import__("exercise").Cache

print("=== Testing decorator with multiple instances ===")

# First instance
cache1 = Cache()
cache1.store(b"data1")
cache1.store(b"data2")
count1 = cache1.get(cache1.store.__qualname__)
print(f"Cache1 count after 2 stores: {count1}")

# Second instance (should share the same counter due to Redis)
cache2 = Cache()  # This will flushdb, resetting counters
cache2.store(b"data3")
count2 = cache2.get(cache2.store.__qualname__)
print(f"Cache2 count after 1 store (new instance): {count2}")

# Add more to cache2
cache2.store(b"data4")
cache2.store(b"data5")
count2_after = cache2.get(cache2.store.__qualname__)
print(f"Cache2 count after 3 total stores: {count2_after}")

print("\n✅ Multiple instances test completed!")
