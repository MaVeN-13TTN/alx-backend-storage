#!/usr/bin/env python3
"""
Final verification test for the requirements
"""

import time
from web import get_page, get_access_count


def test_requirements():
    """Test the specific requirements from the failing tests"""

    # Use a unique URL to ensure fresh state
    url = f"http://httpbin.org/uuid?test={int(time.time())}"

    print("Testing requirements:")
    print(f"URL: {url}")

    # Test 1: Initial count should be 0
    initial_count = get_access_count(url)
    print(f"1. Initial count: {initial_count} (should be 0)")

    # Test 2: Count increments when get_page is called
    get_page(url)
    count_after_first = get_access_count(url)
    print(f"2. Count after first call: {count_after_first} (should be 1)")

    get_page(url)  # This should hit cache
    count_after_second = get_access_count(url)
    print(f"3. Count after second call: {count_after_second} (should be 2)")

    # Test 3: Cache expires after 10 seconds and count resets to 0
    print("4. Waiting 11 seconds for expiration...")
    time.sleep(11)

    count_after_expiry = get_access_count(url)
    print(f"5. Count after expiration: {count_after_expiry} (should be 0)")

    # Test 4: New call after expiration starts fresh
    get_page(url)
    count_after_new_call = get_access_count(url)
    print(f"6. Count after new call: {count_after_new_call} (should be 1)")

    # Summary
    print("\n=== Test Results ===")
    print(f"✓ Initial count is 0: {initial_count == 0}")
    print(
        f"✓ Count increments on calls: {count_after_first == 1 and count_after_second == 2}"
    )
    print(f"✓ Count resets after 10 seconds: {count_after_expiry == 0}")
    print(f"✓ Fresh start after expiry: {count_after_new_call == 1}")

    all_passed = (
        initial_count == 0
        and count_after_first == 1
        and count_after_second == 2
        and count_after_expiry == 0
        and count_after_new_call == 1
    )

    print(f"\n🎯 ALL TESTS PASSED: {all_passed}")
    return all_passed


if __name__ == "__main__":
    test_requirements()
