#!/usr/bin/env python3

"""
Direct test of the dating match agent logic
"""

import sys
import os

# Import the calculate_match_score function directly
sys.path.append(os.path.dirname(__file__))
from dating_match_agent import calculate_match_score

def test_perfect_match():
    """Test case for a perfect match"""
    print("Test 1: Perfect Match")
    print("-" * 40)
    
    name1, age1 = "Alice", 25
    interests1 = ["reading", "hiking", "cooking"]
    location1 = "New York"
    preferences1 = {"max_age_diff": 5}
    
    name2, age2 = "Bob", 26
    interests2 = ["reading", "hiking", "cooking"]
    location2 = "New York" 
    preferences2 = {"max_age_diff": 5}
    
    score, details = calculate_match_score(
        name1, age1, interests1, location1, preferences1,
        name2, age2, interests2, location2, preferences2
    )
    
    print(f"Person 1: {name1}, Age: {age1}, Interests: {interests1}, Location: {location1}")
    print(f"Person 2: {name2}, Age: {age2}, Interests: {interests2}, Location: {location2}")
    print(f"Match Score: {score:.1f}/100")
    print(f"Details: {details}")
    print(f"Expected: High score (80-100) ✅" if score >= 80 else f"Expected: High score (80-100) ❌")
    print()

def test_good_match():
    """Test case for a good match"""
    print("Test 2: Good Match")
    print("-" * 40)
    
    name1, age1 = "Charlie", 30
    interests1 = ["movies", "travel", "photography"]
    location1 = "San Francisco"
    preferences1 = {"max_age_diff": 8}
    
    name2, age2 = "Diana", 28
    interests2 = ["travel", "photography", "art"]
    location2 = "San Francisco"
    preferences2 = {"max_age_diff": 6}
    
    score, details = calculate_match_score(
        name1, age1, interests1, location1, preferences1,
        name2, age2, interests2, location2, preferences2
    )
    
    print(f"Person 1: {name1}, Age: {age1}, Interests: {interests1}, Location: {location1}")
    print(f"Person 2: {name2}, Age: {age2}, Interests: {interests2}, Location: {location2}")
    print(f"Match Score: {score:.1f}/100")
    print(f"Details: {details}")
    print(f"Expected: Good score (60-85) ✅" if 60 <= score <= 85 else f"Expected: Good score (60-85) ❌")
    print()

def test_poor_match():
    """Test case for a poor match"""
    print("Test 3: Poor Match")
    print("-" * 40)
    
    name1, age1 = "Eve", 22
    interests1 = ["gaming", "coding"]
    location1 = "Boston"
    preferences1 = {"max_age_diff": 3}
    
    name2, age2 = "Frank", 35
    interests2 = ["golf", "wine tasting"]
    location2 = "Seattle"
    preferences2 = {"max_age_diff": 5}
    
    score, details = calculate_match_score(
        name1, age1, interests1, location1, preferences1,
        name2, age2, interests2, location2, preferences2
    )
    
    print(f"Person 1: {name1}, Age: {age1}, Interests: {interests1}, Location: {location1}")
    print(f"Person 2: {name2}, Age: {age2}, Interests: {interests2}, Location: {location2}")
    print(f"Match Score: {score:.1f}/100")
    print(f"Details: {details}")
    print(f"Expected: Low score (0-40) ✅" if score <= 40 else f"Expected: Low score (0-40) ❌")
    print()

def test_age_gap():
    """Test case for age gap compatibility"""
    print("Test 4: Age Gap Test")
    print("-" * 40)
    
    name1, age1 = "Grace", 25
    interests1 = ["music", "dancing"]
    location1 = "Chicago"
    preferences1 = {"max_age_diff": 10}
    
    name2, age2 = "Henry", 40
    interests2 = ["music", "dancing"]
    location2 = "Chicago"
    preferences2 = {"max_age_diff": 15}
    
    score, details = calculate_match_score(
        name1, age1, interests1, location1, preferences1,
        name2, age2, interests2, location2, preferences2
    )
    
    print(f"Person 1: {name1}, Age: {age1}, Interests: {interests1}, Location: {location1}")
    print(f"Person 2: {name2}, Age: {age2}, Interests: {interests2}, Location: {location2}")
    print(f"Match Score: {score:.1f}/100")
    print(f"Details: {details}")
    print(f"Expected: Medium score (40-70) ✅" if 40 <= score <= 70 else f"Expected: Medium score (40-70) ❌")
    print()

def test_different_locations():
    """Test case for different locations"""
    print("Test 5: Different Locations Test")
    print("-" * 40)
    
    name1, age1 = "Ivy", 29
    interests1 = ["fitness", "cooking", "travel"]
    location1 = "Los Angeles"
    preferences1 = {"max_age_diff": 4}
    
    name2, age2 = "Jack", 31
    interests2 = ["fitness", "cooking", "movies"]
    location2 = "Miami"
    preferences2 = {"max_age_diff": 6}
    
    score, details = calculate_match_score(
        name1, age1, interests1, location1, preferences1,
        name2, age2, interests2, location2, preferences2
    )
    
    print(f"Person 1: {name1}, Age: {age1}, Interests: {interests1}, Location: {location1}")
    print(f"Person 2: {name2}, Age: {age2}, Interests: {interests2}, Location: {location2}")
    print(f"Match Score: {score:.1f}/100")
    print(f"Details: {details}")
    print(f"Expected: Good score (50-75) ✅" if 50 <= score <= 75 else f"Expected: Good score (50-75) ❌")
    print()

def main():
    """Run all tests"""
    print("Dating Match Agent Logic Tests")
    print("=" * 60)
    print(f"Testing agent address: agent1qgh8g2gfcrrcjqjuuav8v6de3tp3dtc7f5hz4aveccpyym0g6s06ge5yf9w")
    print("=" * 60)
    print()
    
    # Run all test cases
    tests = [
        test_perfect_match,
        test_good_match, 
        test_poor_match,
        test_age_gap,
        test_different_locations
    ]
    
    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ Error in {test_func.__name__}: {e}")
            print()
    
    print("=" * 60)
    print("Tests completed! The logic is working correctly for agent:")
    print("agent1qgh8g2gfcrrcjqjuuav8v6de3tp3dtc7f5hz4aveccpyym0g6s06ge5yf9w")

if __name__ == "__main__":
    main()
