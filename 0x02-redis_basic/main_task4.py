#!/usr/bin/env python3
"""
Test file for replay function - exact requirements
"""
from exercise import Cache, replay

cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
