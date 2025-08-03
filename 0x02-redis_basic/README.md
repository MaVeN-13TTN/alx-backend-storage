# 0x02. Redis basic

This project demonstrates basic Redis operations using Python. It includes implementing a Cache class that stores data in Redis with randomly generated keys, retrieves it with optional type conversion, tracks method call counts, and maintains call history using decorators.

## Learning Objectives

- Learn how to use Redis for basic operations
- Learn how to use Redis as a simple cache
- Understand Redis data types and storage mechanisms
- Practice type annotations in Python
- Learn how to handle data type conversion when retrieving from Redis
- Understand Redis's byte string storage format
- Learn to implement decorators with functools.wraps
- Understand Redis INCR command for atomic incrementing
- Practice method call tracking and monitoring
- Learn Redis list commands (RPUSH, LPUSH, LRANGE)
- Implement call history tracking with input/output storage

## Requirements

- All files interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All files should end with a new line
- First line of all files should be exactly `#!/usr/bin/env python3`
- Code should use the pycodestyle style (version 2.5)
- All modules, classes, and functions should have documentation
- All functions and coroutines must be type-annotated

## Installation

### Redis Server

```bash
sudo apt-get -y install redis-server
pip3 install redis
sudo sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
```

### Start Redis Server

```bash
service redis-server start
```

## Files

- `exercise.py`: Contains the Cache class implementation with store/get methods and decorators
- `main.py`: Test file for the Cache class (Task 0)
- `main_task2.py`: Test file for count_calls decorator (Task 2)
- `main_task3.py`: Test file for call_history decorator (Task 3)
- `test_task1.py`: Test file for get methods (Task 1)
- `test_get_methods.py`: Additional tests for get_str and get_int methods
- `test_count_calls.py`: Comprehensive tests for the count_calls decorator
- `test_call_history.py`: Comprehensive tests for the call_history decorator
- `test_multiple_instances.py`: Tests decorator behavior with multiple Cache instances
- `comprehensive_test.py`: Complete test suite for all implemented features

## Usage

### Basic Usage (Task 0)

```python
#!/usr/bin/env python3
import redis

Cache = __import__('exercise').Cache

cache = Cache()
data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))
```

### Using Get Methods (Task 1)

```python
#!/usr/bin/env python3
Cache = __import__('exercise').Cache

cache = Cache()

# Store different data types
str_key = cache.store("hello world")
int_key = cache.store(42)
bytes_key = cache.store(b"byte data")

# Retrieve with type conversion
print(cache.get_str(str_key))  # Returns: "hello world"
print(cache.get_int(int_key))  # Returns: 42
print(cache.get(bytes_key))    # Returns: b"byte data"

# Custom conversion function
result = cache.get(str_key, fn=lambda d: d.decode("utf-8").upper())
print(result)  # Returns: "HELLO WORLD"
```

### Counting Method Calls (Task 2)

```python
#!/usr/bin/env python3
Cache = __import__('exercise').Cache

cache = Cache()

# Each store call increments the counter
cache.store(b"first")
print(cache.get(cache.store.__qualname__))  # Returns: b'1'

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))  # Returns: b'3'

# Check the method's qualified name used as key
print(f"Counter key: {cache.store.__qualname__}")  # Returns: Cache.store
```

### Storing Call History (Task 3)
```python
#!/usr/bin/env python3
Cache = __import__('exercise').Cache

cache = Cache()

# Store some data
s1 = cache.store("first")
s2 = cache.store("second")
s3 = cache.store("third")

# Retrieve input and output history
inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs:", inputs)   # [b"('first',)", b"('second',)", b"('third',)"]
print("outputs:", outputs) # [b'key1', b'key2', b'key3']
```

## Tasks

### 0. Writing strings to Redis

Create a Cache class with:

- `__init__` method that stores a Redis client instance and flushes the database
- `store` method that generates a random key, stores data, and returns the key
- Proper type annotations for data types: str, bytes, int, float

**Key Features:**

- Uses UUID4 for random key generation
- Supports multiple data types (str, bytes, int, float)
- Flushes Redis database on initialization for clean state

### 1. Reading from Redis and recovering original type

Extend the Cache class with data retrieval methods:

- `get` method that takes a key and optional conversion function
- `get_str` method for automatic string conversion
- `get_int` method for automatic integer conversion

**Key Features:**

- Redis stores all data as bytes, but methods can convert back to original types
- `get(key, fn=None)` - retrieves data with optional conversion function
- `get_str(key)` - automatically decodes bytes to UTF-8 string
- `get_int(key)` - automatically converts bytes to integer
- Returns `None` for non-existent keys (preserves Redis.get behavior)
- Supports custom conversion functions via callable parameter

**Example Test Case:**

```python
cache = Cache()
TEST_CASES = {
    b"foo": None,                           # bytes, no conversion
    123: int,                              # int with int conversion
    "bar": lambda d: d.decode("utf-8")     # string with decode
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value  # All assertions pass
```

### 2. Incrementing values

Implement a system to count how many times methods are called using a decorator:

- Create `count_calls` decorator above the Cache class
- Decorator uses method's `__qualname__` as Redis key
- Uses Redis INCR command to atomically increment counter
- Decorate the `store` method with `@count_calls`

**Key Features:**

- **Decorator Pattern**: Uses `functools.wraps` to preserve original method metadata
- **Atomic Counting**: Uses Redis INCR for thread-safe incrementing
- **Method Tracking**: Tracks calls specifically using method's qualified name
- **Preserved Functionality**: Decorated method works exactly like the original
- **Redis Integration**: Counter stored in same Redis instance as cache data

**Implementation Details:**

```python
def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # "Cache.store"
        self._redis.incr(key)      # Increment counter
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    @count_calls
    def store(self, data):
        # Original store implementation
```

**Example Test Case:**

```python
cache = Cache()
cache.store(b"first")   # Counter = 1
cache.store(b"second")  # Counter = 2
cache.store(b"third")   # Counter = 3
count = cache.get(cache.store.__qualname__)  # Returns b'3'
```

### 3. Storing lists

Implement a decorator to store the history of inputs and outputs for a function:
- Create `call_history` decorator above the Cache class
- Decorator stores function inputs and outputs in separate Redis lists
- Uses `method.__qualname__` with `:inputs` and `:outputs` suffixes as keys
- Uses Redis RPUSH command to append to lists
- Apply both `@call_history` and `@count_calls` decorators to store method

**Key Features:**
- **Input/Output Tracking**: Stores complete call history with arguments and results
- **Redis Lists**: Uses RPUSH to maintain chronological order
- **Qualified Name Keys**: Uses `Cache.store:inputs` and `Cache.store:outputs` as keys
- **String Normalization**: Converts arguments to strings using `str(args)`
- **Decorator Stacking**: Works together with `count_calls` decorator

**Implementation Details:**
```python
def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Store input arguments
        self._redis.rpush(input_key, str(args))
        
        # Execute method and store output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        
        return output
    return wrapper

class Cache:
    @call_history
    @count_calls
    def store(self, data):
        # Original store implementation
```

**Example Test Case:**
```python
cache = Cache()
cache.store("first")
cache.store("second")
cache.store("third")

inputs = cache._redis.lrange("Cache.store:inputs", 0, -1)
outputs = cache._redis.lrange("Cache.store:outputs", 0, -1)
# inputs: [b"('first',)", b"('second',)", b"('third',)"]
# outputs: [b'key1', b'key2', b'key3']
```

## Cache Class Methods

### Decorators

- `call_history(method: Callable) -> Callable`
  - Decorator that stores the history of inputs and outputs for a function
  - Uses `method.__qualname__:inputs` and `method.__qualname__:outputs` as Redis keys
  - Uses Redis RPUSH command to append arguments and results to lists
  - Converts arguments to strings for Redis storage

- `count_calls(method: Callable) -> Callable`
  - Decorator that counts how many times a method is called
  - Uses method's `__qualname__` as Redis key for counter
  - Uses Redis INCR command for atomic incrementing
  - Preserves original method metadata with `functools.wraps`

### Storage Methods

- `store(data: Union[str, bytes, int, float]) -> str` (decorated with @call_history and @count_calls)
  - Stores data in Redis with a randomly generated UUID key
  - Returns the generated key as a string
  - Each call increments a counter stored in Redis
  - Each call stores input arguments and output in separate Redis lists

### Retrieval Methods

- `get(key: str, fn: Optional[Callable] = None) -> Any`

  - Retrieves data from Redis using the provided key
  - Optionally applies conversion function `fn` to the retrieved bytes
  - Returns `None` if key doesn't exist

- `get_str(key: str) -> Optional[str]`

  - Convenience method to retrieve and decode data as UTF-8 string
  - Equivalent to `get(key, fn=lambda d: d.decode("utf-8"))`

- `get_int(key: str) -> Optional[int]`
  - Convenience method to retrieve and convert data to integer
  - Equivalent to `get(key, fn=int)`

## Testing

Run the comprehensive test suite:

```bash
python3 comprehensive_test.py
```

Run individual tests:

```bash
python3 main.py                    # Test basic store functionality (Task 0)
python3 main_task2.py              # Test count_calls decorator (Task 2)
python3 main_task3.py              # Test call_history decorator (Task 3)
python3 test_task1.py              # Test get method with required test cases (Task 1)
python3 test_get_methods.py        # Test get_str and get_int methods
python3 test_count_calls.py        # Comprehensive decorator tests
python3 test_call_history.py       # Comprehensive call_history tests
python3 test_multiple_instances.py # Test decorator with multiple instances
```

### Expected Output Examples

**Task 0 (Basic Storage):**

```bash
$ python3 main.py
3a3e8231-b2f6-450d-8b0e-0f38f16e8ca2
b'hello'
```

**Task 2 (Method Counting):**

```bash
$ python3 main_task2.py
b'1'
b'3'
```

**Task 3 (Call History):**
```bash
$ python3 main_task3.py
04f8dcaa-d354-4221-87f3-4923393a25ad
a160a8a8-06dc-4934-8e95-df0cb839644b  
15a8fd87-1f55-4059-86aa-9d1a0d4f2aea
inputs: [b"('first',)", b"('secont',)", b"('third',)"]
outputs: [b'04f8dcaa-d354-4221-87f3-4923393a25ad', b'a160a8a8-06dc-4934-8e95-df0cb839644b', b'15a8fd87-1f55-4059-86aa-9d1a0d4f2aea']
```
