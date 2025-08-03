#!/usr/bin/env python3
"""
Test with Google.com to verify fresh behavior
"""

import time
from web import get_page, get_access_count

if __name__ == "__main__":
    url = "http://google.com"

    print("=== Testing with Google.com ===")
    print(f"URL: {url}")

    # Check initial count (should be 0 for a fresh URL)
    initial_count = get_access_count(url)
    print(f"Initial count: {initial_count}")

    if initial_count > 0:
        print("Clearing existing data...")
        # Let's use a unique URL to ensure fresh start
        url = f"http://google.com?test={int(time.time())}"
        print(f"Using fresh URL: {url}")

    print(f"Initial count for fresh URL: {get_access_count(url)}")

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

    # Wait for expiration
    print("\n3. Waiting 11 seconds for cache expiration...")
    time.sleep(11)

    # Check count after expiration
    count_after_expiry = get_access_count(url)
    print(f"Count after cache expiry: {count_after_expiry}")

    print(f"\n=== Test Results ===")
    print(f"✓ Count starts at 0: {initial_count == 0 or get_access_count(url) == 0}")
    print(f"✓ Count increments on calls: {count1 == 1 and count2 == 2}")
    print(f"✓ Count resets after expiration: {count_after_expiry == 0}")
