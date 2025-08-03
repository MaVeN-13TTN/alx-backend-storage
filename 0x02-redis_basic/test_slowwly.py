#!/usr/bin/env python3
"""
Test with slowwly.co.uk URL as suggested in the task
"""

import time
from web import get_page, get_access_count

if __name__ == "__main__":
    # Use slowwly to simulate slow response as suggested in the task
    slow_url = (
        "http://slowwly.robertomurray.co.uk/delay/2000/url/http://httpbin.org/uuid"
    )

    print(f"=== Testing with slowwly URL ===")
    print(f"URL: {slow_url}")
    print(f"Initial access count: {get_access_count(slow_url)}")

    # First call - should take ~2 seconds
    print("\n1. First call (from web - should be slow):")
    start = time.time()
    result1 = get_page(slow_url)
    duration1 = time.time() - start
    print(f"Time taken: {duration1:.2f}s")
    print(f"Access count: {get_access_count(slow_url)}")
    print(f"Content preview: {result1[:100]}...")

    # Second call - should be instant (from cache)
    print("\n2. Second call (from cache - should be fast):")
    start = time.time()
    result2 = get_page(slow_url)
    duration2 = time.time() - start
    print(f"Time taken: {duration2:.4f}s")
    print(f"Access count: {get_access_count(slow_url)}")
    print(f"Same content: {result1 == result2}")

    print(f"\nSpeed improvement: {duration1/duration2:.0f}x faster!")
    print(f"Total accesses: {get_access_count(slow_url)}")
