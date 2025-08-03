#!/usr/bin/env python3
"""
Simple test for web.py functionality
"""

from web import get_page, get_access_count
import time

if __name__ == "__main__":
    url = "http://httpbin.org/get"

    print(f"Testing URL: {url}")
    print(f"Initial access count: {get_access_count(url)}")

    # First call - should fetch from web
    print("\nFirst call (fetch from web):")
    start = time.time()
    result1 = get_page(url)
    print(f"Time taken: {time.time() - start:.3f}s")
    print(f"Access count: {get_access_count(url)}")
    print(f"Content preview: {result1[:100]}...")

    # Second call - should use cache
    print("\nSecond call (from cache):")
    start = time.time()
    result2 = get_page(url)
    print(f"Time taken: {time.time() - start:.3f}s")
    print(f"Access count: {get_access_count(url)}")
    print(f"Same content: {result1 == result2}")
