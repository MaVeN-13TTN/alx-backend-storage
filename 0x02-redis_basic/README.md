# 0x02. Redis basic

This project demonstrates basic Redis operations using Python. It includes implementing a Cache class that stores data in Redis with randomly generated keys, retrieves it with optional type conversion, tracks method call counts, maintains call history using decorators, provides replay functionality to display function call history, and implements an expiring web cache with request tracking.

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
- Create replay functionality to display function call history
- Practice using zip() function for data pairing
- Learn to implement web caching with expiration using Redis SETEX
- Understand HTTP request optimization through caching
- Practice decorator patterns for clean separation of concerns
- Learn to track URL access patterns and statistics

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

- `exercise.py`: Contains the Cache class implementation with store/get methods, decorators, and replay function
- `web.py`: Web caching implementation with expiration and request tracking (Task 5)
- `main.py`: Test file for the Cache class (Task 0)
- `main_task2.py`: Test file for count_calls decorator (Task 2)
- `main_task3.py`: Test file for call_history decorator (Task 3)
- `main_task4.py`: Test file for replay function (Task 4)
- `main_task5.py`: Test file for web caching functionality (Task 5)
- `test_task1.py`: Test file for get methods (Task 1)
- `test_get_methods.py`: Additional tests for get_str and get_int methods
- `test_count_calls.py`: Comprehensive tests for the count_calls decorator
- `test_call_history.py`: Comprehensive tests for the call_history decorator
- `test_replay.py`: Basic tests for the replay function
- `test_replay_comprehensive.py`: Comprehensive tests for the replay function
- `test_multiple_instances.py`: Tests decorator behavior with multiple Cache instances
- `test_web.py`: Simple tests for web caching functionality
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

**Task 3 (Call History):**

```bash
$ python3 main_task3.py
[b'key1', b'key2', b'key3']
```

**Task 4 (Replay Function):**

```bash
$ python3 main_task4.py
Cache.store was called 4 times:
Cache.store(*('first',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
Cache.store(*('second',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
Cache.store(*([1, 2, 3],)) -> d686d562-229a-4a6d-8b8e-7dcbe7f54c18
```

### Displaying Call History (Task 4)

```python
#!/usr/bin/env python3
from exercise import Cache, replay

cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)
# Output:
# Cache.store was called 3 times:
# Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
# Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
# Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
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

### 4. Retrieving lists

Implement a replay function to display the history of calls of a particular function:

- Create `replay` function that takes a bound method as parameter
- Uses keys generated from previous tasks to display call history
- Shows total number of calls and each call with its input/output
- Uses Redis LRANGE command and zip() to iterate over inputs and outputs

**Key Features:**

- **History Display**: Shows formatted call history with inputs and outputs
- **Redis LRANGE**: Uses LRANGE command to retrieve list data
- **Data Pairing**: Uses zip() function to pair inputs with outputs
- **Bound Method Access**: Accesses Redis instance through method's `__self__` attribute
- **Formatted Output**: Displays calls in human-readable format

**Implementation Details:**

```python
def replay(method) -> None:
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    # Get call count and history
    count = redis_instance.get(method_name)
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    # Display formatted history
    print(f"{method_name} was called {count} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")
```

**Example Output:**

```
Cache.store was called 3 times:
Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
```

### 5. Implementing an expiring web cache and tracker

Implement a web cache with expiration and request tracking using Redis:

- Create `get_page` function that fetches HTML content from URLs
- Track access count for each URL in key "count:{url}"
- Cache results with 10 seconds expiration time
- Use decorator pattern for clean implementation

**Key Features:**

- **URL Tracking**: Counts how many times each URL was accessed
- **Expiring Cache**: Stores web content with automatic expiration
- **Request Optimization**: Reduces network calls by caching responses
- **Decorator Implementation**: Clean separation of caching logic
- **Redis SETEX**: Uses SETEX command for cache with expiration

**Implementation Details:**

```python
@cache_with_expiration(10)
def get_page(url: str) -> str:
    """Fetch HTML content with caching and tracking."""
    response = requests.get(url)
    return response.text

def get_access_count(url: str) -> int:
    """Get the number of times a URL was accessed."""
    count = _redis.get(f"count:{url}")
    return int(count.decode('utf-8')) if count is not None else 0
```

**Example Usage:**

```python
from web import get_page, get_access_count

# First call - fetches from web (slower)
content = get_page("http://example.com")
print(f"Access count: {get_access_count('http://example.com')}")  # 1

# Second call - uses cache (faster)
content = get_page("http://example.com")
print(f"Access count: {get_access_count('http://example.com')}")  # 2

# After 10 seconds, cache expires and next call fetches from web again
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
python3 main_task4.py              # Test replay function (Task 4)
python3 main_task5.py              # Test web caching functionality (Task 5)
python3 test_task1.py              # Test get method with required test cases (Task 1)
python3 test_get_methods.py        # Test get_str and get_int methods
python3 test_count_calls.py        # Comprehensive decorator tests
python3 test_call_history.py       # Comprehensive call_history tests
python3 test_multiple_instances.py # Test decorator with multiple instances
python3 test_replay.py             # Comprehensive replay function tests
python3 test_web.py                # Simple tests for web caching functionality
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

**Task 5 (Web Caching):**

```bash
$ python3 test_web.py
Testing URL: http://httpbin.org/get
Initial access count: 0

First call (fetch from web):
Time taken: 0.513s
Access count: 1
Content preview: {
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "...

Second call (from cache):
Time taken: 0.000s
Access count: 2
Same content: True
```
