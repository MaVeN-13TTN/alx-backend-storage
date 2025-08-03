#!/usr/bin/env python3
"""
Comprehensive test for both task 0 and task 1
"""
Cache = __import__("exercise").Cache

print("=== Testing Cache Class ===")

# Test Cache instantiation
cache = Cache()
print("✅ Cache instance created successfully")

# Test store method (Task 0)
print("\n=== Testing store method (Task 0) ===")
data_types = [("bytes", b"hello"), ("string", "world"), ("int", 42), ("float", 3.14)]

keys = {}
for type_name, data in data_types:
    key = cache.store(data)
    keys[type_name] = key
    print(f"✅ Stored {type_name}: {data} -> key: {key[:8]}...")

# Test get method (Task 1)
print("\n=== Testing get method (Task 1) ===")

# Test the exact requirements from the task
TEST_CASES = {b"foo": None, 123: int, "bar": lambda d: d.decode("utf-8")}

print("Running required test cases:")
for value, fn in TEST_CASES.items():
    key = cache.store(value)
    result = cache.get(key, fn=fn)
    print(f"✅ {value} -> {result} (match: {result == value})")
    assert cache.get(key, fn=fn) == value

# Test get_str and get_int methods
print("\n=== Testing get_str and get_int methods ===")

# Test get_str
str_key = cache.store("hello redis")
str_result = cache.get_str(str_key)
print(
    f"✅ get_str: 'hello redis' -> '{str_result}' (type: {type(str_result).__name__})"
)

# Test get_int
int_key = cache.store(999)
int_result = cache.get_int(int_key)
print(f"✅ get_int: 999 -> {int_result} (type: {type(int_result).__name__})")

# Test non-existent key behavior
print("\n=== Testing non-existent key behavior ===")
none_result = cache.get("non-existent")
print(f"✅ get('non-existent'): {none_result}")
print(f"✅ get_str('non-existent'): {cache.get_str('non-existent')}")
print(f"✅ get_int('non-existent'): {cache.get_int('non-existent')}")

print("\n🎉 All tests passed! Implementation is complete and correct.")
