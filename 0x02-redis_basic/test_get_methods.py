#!/usr/bin/env python3
"""
Test file for get_str and get_int methods
"""
Cache = __import__("exercise").Cache

cache = Cache()

# Test get_str
print("Testing get_str method:")
str_key = cache.store("hello world")
result_str = cache.get_str(str_key)
print(f"Stored: 'hello world' (str)")
print(f"Retrieved with get_str: {result_str} ({type(result_str).__name__})")
print(f"Match: {result_str == 'hello world'}")
print()

# Test get_int
print("Testing get_int method:")
int_key = cache.store(42)
result_int = cache.get_int(int_key)
print(f"Stored: 42 (int)")
print(f"Retrieved with get_int: {result_int} ({type(result_int).__name__})")
print(f"Match: {result_int == 42}")
print()

# Test with non-existent key
print("Testing with non-existent key:")
non_existent = cache.get("non-existent-key")
print(f"get('non-existent-key'): {non_existent}")
print(f"get_str('non-existent-key'): {cache.get_str('non-existent-key')}")
print(f"get_int('non-existent-key'): {cache.get_int('non-existent-key')}")
print()

# Test get method without fn (should return bytes)
print("Testing get method without fn:")
test_key = cache.store("test string")
raw_result = cache.get(test_key)
print(f"Stored: 'test string' (str)")
print(f"Retrieved with get (no fn): {raw_result} ({type(raw_result).__name__})")
print()

print("All tests completed successfully!")
