#!/usr/bin/env python3
"""
Test to verify cache and count expiration behavior
"""

import time
from web import get_page, get_access_count

if __name__ == "__main__":
    url = "http://httpbin.org/get"

    print("=== Testing Cache and Count Expiration ===")
    print(f"URL: {url}")

    # Clear any existing data
    print(f"Initial count: {get_access_count(url)}")

    # First call
    print("\n1. First call:")
    get_page(url)
    count1 = get_access_count(url)
    print(f"Count after first call: {count1}")

    # Second call (should be cached)
    print("\n2. Second call (cached):")
    get_page(url)
    count2 = get_access_count(url)
    print(f"Count after second call: {count2}")

    # Third call (still cached)
    print("\n3. Third call (still cached):")
    get_page(url)
    count3 = get_access_count(url)
    print(f"Count after third call: {count3}")

    # Wait for expiration
    print("\n4. Waiting 11 seconds for cache expiration...")
    time.sleep(11)

    # Check count after expiration
    count_after_expiry = get_access_count(url)
    print(f"Count after cache expiry: {count_after_expiry}")

    # Call again after expiration
    print("\n5. Call after expiration:")
    get_page(url)
    count_final = get_access_count(url)
    print(f"Count after new call: {count_final}")

    print(f"\n=== Results ===")
    print(
        f"Count progression: {count1} -> {count2} -> {count3} -> {count_after_expiry} -> {count_final}"
    )
    print(f"Count resets after expiration: {count_after_expiry == 0}")
    print(f"Count increments properly: {count_final == 1}")
