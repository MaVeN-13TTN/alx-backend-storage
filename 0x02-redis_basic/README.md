# 0x02. Redis basic

This project demonstrates basic Redis operations using Python. It includes implementing a Cache class that stores data in Redis with randomly generated keys.

## Learning Objectives

- Learn how to use Redis for basic operations
- Learn how to use Redis as a simple cache
- Understand Redis data types and storage mechanisms
- Practice type annotations in Python

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

- `exercise.py`: Contains the Cache class implementation
- `main.py`: Test file for the Cache class

## Usage

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

## Tasks

### 0. Writing strings to Redis

Create a Cache class with:

- `__init__` method that stores a Redis client instance and flushes the database
- `store` method that generates a random key, stores data, and returns the key
- Proper type annotations for data types: str, bytes, int, float
