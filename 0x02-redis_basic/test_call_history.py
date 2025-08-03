#!/usr/bin/env python3
"""
Test file for call_history decorator
"""
Cache = __import__('exercise').Cache

print("=== Testing call_history decorator ===")

cache = Cache()

# Test with different data types
test_data = ["first", "second", 42, 3.14, b"bytes"]

print("Storing test data:")
for i, data in enumerate(test_data):
    key = cache.store(data)
    print(f"{i+1}. Stored {data} -> {key}")

# Check the input and output history
input_key = f"{cache.store.__qualname__}:inputs"
output_key = f"{cache.store.__qualname__}:outputs"

inputs = cache._redis.lrange(input_key, 0, -1)
outputs = cache._redis.lrange(output_key, 0, -1)

print(f"\nInput history ({input_key}):")
for i, inp in enumerate(inputs):
    print(f"  {i+1}. {inp}")

print(f"\nOutput history ({output_key}):")
for i, out in enumerate(outputs):
    print(f"  {i+1}. {out}")

print(f"\nTotal calls stored: {len(inputs)}")
print(f"Input/Output lists match: {len(inputs) == len(outputs)}")

# Test that both decorators work together
count = cache.get(cache.store.__qualname__)
print(f"Call count from count_calls decorator: {count}")

print("\n✅ All tests completed!")
