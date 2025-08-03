#!/usr/bin/env python3
"""
Test file for web.py - Task 5
"""

import time
from web import get_page, get_access_count

if __name__ == "__main__":
    # Test URL (using slowwly for testing as suggested)
    slow_url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
    fast_url = "http://httpbin.org/delay/1"

    print("=== Testing Web Cache with Expiration ===")

    # Test 1: First access (should fetch from web)
    print(f"\n1. First access to {fast_url}")
    print(f"Access count before: {get_access_count(fast_url)}")

    start_time = time.time()
    content1 = get_page(fast_url)
    end_time = time.time()

    print(f"First fetch took: {end_time - start_time:.2f} seconds")
    print(f"Content length: {len(content1)} characters")
    print(f"Access count after: {get_access_count(fast_url)}")

    # Test 2: Immediate second access (should use cache)
    print(f"\n2. Immediate second access (should use cache)")
    print(f"Access count before: {get_access_count(fast_url)}")

    start_time = time.time()
    content2 = get_page(fast_url)
    end_time = time.time()

    print(f"Cached fetch took: {end_time - start_time:.4f} seconds")
    print(f"Content identical: {content1 == content2}")
    print(f"Access count after: {get_access_count(fast_url)}")

    # Test 3: Third access (still cached)
    print(f"\n3. Third access (still cached)")
    print(f"Access count before: {get_access_count(fast_url)}")

    content3 = get_page(fast_url)
    print(f"Access count after: {get_access_count(fast_url)}")

    # Test 4: Wait for cache expiration
    print(f"\n4. Waiting for cache expiration (11 seconds)...")
    time.sleep(11)

    print(f"Access count before: {get_access_count(fast_url)}")

    start_time = time.time()
    content4 = get_page(fast_url)
    end_time = time.time()

    print(f"Post-expiration fetch took: {end_time - start_time:.2f} seconds")
    print(f"Access count after: {get_access_count(fast_url)}")

    print(f"\n=== Final Statistics ===")
    print(f"Total accesses to {fast_url}: {get_access_count(fast_url)}")
