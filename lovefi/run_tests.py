#!/usr/bin/env python3

import asyncio
import aiohttp
import json
from typing import List, Dict

# Define the test data structure to match the agent's expected input
class TestCase:
    def __init__(self, name: str, data: Dict, expected_score_range: tuple = None):
        self.name = name
        self.data = data
        self.expected_score_range = expected_score_range

# Test cases
test_cases = [
    TestCase(
        name="Perfect Match Test",
        data={
            "name1": "Alice",
            "age1": 25,
            "interests1": ["reading", "hiking", "cooking"],
            "location1": "New York",
            "preferences1": {"max_age_diff": 5},
            "name2": "Bob",
            "age2": 26,
            "interests2": ["reading", "hiking", "cooking"],
            "location2": "New York",
            "preferences2": {"max_age_diff": 5}
        },
        expected_score_range=(80, 100)
    ),
    TestCase(
        name="Good Match Test",
        data={
            "name1": "Charlie",
            "age1": 30,
            "interests1": ["movies", "travel", "photography"],
            "location1": "San Francisco",
            "preferences1": {"max_age_diff": 8},
            "name2": "Diana",
            "age2": 28,
            "interests2": ["travel", "photography", "art"],
            "location2": "San Francisco",
            "preferences2": {"max_age_diff": 6}
        },
        expected_score_range=(60, 85)
    ),
    TestCase(
        name="Poor Match Test",
        data={
            "name1": "Eve",
            "age1": 22,
            "interests1": ["gaming", "coding"],
            "location1": "Boston",
            "preferences1": {"max_age_diff": 3},
            "name2": "Frank",
            "age2": 35,
            "interests2": ["golf", "wine tasting"],
            "location2": "Seattle",
            "preferences2": {"max_age_diff": 5}
        },
        expected_score_range=(0, 40)
    ),
    TestCase(
        name="Age Gap Test",
        data={
            "name1": "Grace",
            "age1": 25,
            "interests1": ["music", "dancing"],
            "location1": "Chicago",
            "preferences1": {"max_age_diff": 10},
            "name2": "Henry",
            "age2": 40,
            "interests2": ["music", "dancing"],
            "location2": "Chicago",
            "preferences2": {"max_age_diff": 15}
        },
        expected_score_range=(40, 70)
    ),
    TestCase(
        name="Different Locations Test",
        data={
            "name1": "Ivy",
            "age1": 29,
            "interests1": ["fitness", "cooking", "travel"],
            "location1": "Los Angeles",
            "preferences1": {"max_age_diff": 4},
            "name2": "Jack",
            "age2": 31,
            "interests2": ["fitness", "cooking", "movies"],
            "location2": "Miami",
            "preferences2": {"max_age_diff": 6}
        },
        expected_score_range=(50, 75)
    )
]

async def send_test_request(agent_address: str, test_case: TestCase):
    """Send a test request to the dating match agent via HTTP"""
    url = "http://localhost:8000/submit"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=test_case.data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"HTTP Error {response.status}: {await response.text()}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

async def run_all_tests(agent_address: str):
    """Run all test cases"""
    print(f"Running tests against agent: {agent_address}")
    print("=" * 60)
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case.name}")
        print("-" * 40)
        
        # Display test data
        data = test_case.data
        print(f"Person 1: {data['name1']}, Age: {data['age1']}, Interests: {data['interests1']}, Location: {data['location1']}")
        print(f"Person 2: {data['name2']}, Age: {data['age2']}, Interests: {data['interests2']}, Location: {data['location2']}")
        
        # Send request
        result = await send_test_request(agent_address, test_case)
        
        if result:
            score = result.get('score', 'N/A')
            details = result.get('details', 'N/A')
            
            print(f"Match Score: {score}")
            print(f"Details: {details}")
            
            # Check if score is in expected range
            if test_case.expected_score_range and isinstance(score, (int, float)):
                min_score, max_score = test_case.expected_score_range
                if min_score <= score <= max_score:
                    status = "✅ PASS"
                else:
                    status = f"❌ FAIL (Expected: {min_score}-{max_score})"
            else:
                status = "⚠️  No expectation set"
            
            print(f"Status: {status}")
            results.append((test_case.name, score, status, True))
        else:
            print("❌ Failed to get response from agent")
            results.append((test_case.name, "N/A", "❌ FAIL - No response", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, _, status, success in results if success and "✅" in status)
    total = len(results)
    
    for name, score, status, _ in results:
        print(f"{name}: {score} - {status}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed or had issues")

def main():
    """Main function to run the tests"""
    agent_address = "agent1qgh8g2gfcrrcjqjuuav8v6de3tp3dtc7f5hz4aveccpyym0g6s06ge5yf9w"
    
    print("Dating Match Agent Test Suite")
    print("=" * 60)
    print(f"Target Agent Address: {agent_address}")
    print("Endpoint: http://localhost:8000/submit")
    print()
    print("Make sure your dating match agent is running on port 8000!")
    print()
    input("Press Enter to start tests...")
    
    # Run the tests
    try:
        asyncio.run(run_all_tests(agent_address))
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n\nError running tests: {e}")

if __name__ == "__main__":
    main()
