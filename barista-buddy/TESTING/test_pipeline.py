"""
Integration Tests for Barista Buddy Pipeline
Tests each component and the full pipeline
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fuzzy_matcher import FuzzyMatcher
from topic_filter import TopicFilter
from retrieval_system import RetrievalSystem


class TestSuite:
    """Test suite for Barista Buddy"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
    
    def test(self, name: str, condition: bool, message: str = ""):
        """Run a single test"""
        self.total += 1
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}")
            if message:
                print(f"    {message}")
    
    def section(self, name: str):
        """Print section header"""
        print(f"\n{'='*70}")
        print(f"  {name}")
        print(f"{'='*70}\n")
    
    def summary(self):
        """Print test summary"""
        print(f"\n{'='*70}")
        print(f"  TEST SUMMARY")
        print(f"{'='*70}")
        print(f"  Total:  {self.total}")
        print(f"  Passed: {self.passed} ✓")
        print(f"  Failed: {self.failed} ✗")
        print(f"  Score:  {(self.passed/self.total*100):.1f}%")
        print(f"{'='*70}\n")


def test_fuzzy_matcher():
    """Test pronunciation correction"""
    suite = TestSuite()
    suite.section("FUZZY MATCHER TESTS")
    
    try:
        matcher = FuzzyMatcher()
        
        # Test direct corrections
        test_cases = [
            ("expresso", "espresso"),
            ("machiato", "macchiato"),
            ("capuccino", "cappuccino"),
            ("lattay", "latte"),
        ]
        
        for input_word, expected in test_cases:
            corrected = matcher.correct_text(input_word)
            suite.test(
                f"Correct '{input_word}' → '{expected}'",
                corrected == expected,
                f"Got: {corrected}"
            )
        
        # Test multi-word
        result = matcher.correct_text("how to make expresso")
        suite.test(
            "Multi-word correction",
            "espresso" in result,
            f"Got: {result}"
        )
        
    except Exception as e:
        suite.test("Fuzzy matcher initialization", False, str(e))
    
    return suite


def test_topic_filter():
    """Test topic filtering"""
    suite = TestSuite()
    suite.section("TOPIC FILTER TESTS")
    
    try:
        filter_obj = TopicFilter()
        
        # Coffee-related queries (should pass)
        coffee_queries = [
            "how to make espresso",
            "what is the best grind size",
            "cappuccino recipe",
            "milk steaming temperature",
            "arabica vs robusta"
        ]
        
        for query in coffee_queries:
            is_related, conf, reason = filter_obj.is_coffee_related(query)
            suite.test(
                f"Accept: '{query}'",
                is_related,
                f"Confidence: {conf:.2f}, Reason: {reason}"
            )
        
        # Non-coffee queries (should fail)
        non_coffee_queries = [
            "what is the weather today",
            "who won the game",
            "how to fix my car",
            "tell me a joke"
        ]
        
        for query in non_coffee_queries:
            is_related, conf, reason = filter_obj.is_coffee_related(query)
            suite.test(
                f"Reject: '{query}'",
                not is_related,
                f"Confidence: {conf:.2f}, Reason: {reason}"
            )
        
    except Exception as e:
        suite.test("Topic filter initialization", False, str(e))
    
    return suite


def test_retrieval_system():
    """Test retrieval system"""
    suite = TestSuite()
    suite.section("RETRIEVAL SYSTEM TESTS")
    
    try:
        retrieval = RetrievalSystem()
        
        # Test retrieval accuracy
        test_queries = [
            ("how to make espresso", "espresso"),
            ("bitter coffee fix", "bitter"),
            ("latte art", "latte"),
            ("grind size for french press", "french press"),
            ("arabica vs robusta", "arabica")
        ]
        
        for query, expected_keyword in test_queries:
            results = retrieval.retrieve(query, top_k=3)
            
            # Check if we got results
            suite.test(
                f"Retrieve: '{query}'",
                len(results) > 0,
                f"Got {len(results)} results"
            )
            
            # Check relevance
            if results:
                answer = results[0]['answer'].lower()
                suite.test(
                    f"Relevant result for '{query}'",
                    expected_keyword.lower() in answer,
                    f"Score: {results[0]['relevance_score']:.3f}"
                )
        
        # Test get_answer
        answer, conf = retrieval.get_answer("how to make espresso")
        suite.test(
            "get_answer returns result",
            len(answer) > 0 and conf > 0,
            f"Confidence: {conf:.3f}"
        )
        
    except Exception as e:
        suite.test("Retrieval system initialization", False, str(e))
    
    return suite


def test_full_pipeline():
    """Test full pipeline integration"""
    suite = TestSuite()
    suite.section("FULL PIPELINE TESTS")
    
    try:
        # Initialize components
        matcher = FuzzyMatcher()
        topic_filter = TopicFilter()
        retrieval = RetrievalSystem()
        
        # Test queries through full pipeline
        test_cases = [
            {
                "input": "how to make expresso",
                "should_pass": True,
                "expected_keyword": "espresso"
            },
            {
                "input": "what is the weather",
                "should_pass": False,
                "expected_keyword": None
            },
            {
                "input": "capuccino recipe",
                "should_pass": True,
                "expected_keyword": "cappuccino"
            }
        ]
        
        for case in test_cases:
            query = case["input"]
            
            # Step 1: Fuzzy matching
            corrected = matcher.correct_text(query)
            
            # Step 2: Topic filtering
            is_related, conf, reason = topic_filter.is_coffee_related(corrected)
            
            suite.test(
                f"Pipeline: '{query}' should {'pass' if case['should_pass'] else 'fail'}",
                is_related == case["should_pass"],
                f"Got: {is_related}, Confidence: {conf:.2f}"
            )
            
            # Step 3: Retrieval (only if passed filter)
            if is_related and case["should_pass"]:
                results = retrieval.retrieve(corrected, top_k=1)
                has_keyword = False
                if results and case["expected_keyword"]:
                    answer = results[0]['answer'].lower()
                    has_keyword = case["expected_keyword"].lower() in answer
                
                suite.test(
                    f"Retrieve relevant answer for '{query}'",
                    has_keyword,
                    f"Score: {results[0]['relevance_score']:.3f}" if results else "No results"
                )
        
    except Exception as e:
        suite.test("Full pipeline", False, str(e))
    
    return suite


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  BARISTA BUDDY - TEST SUITE")
    print("="*70 + "\n")
    
    # Run individual test suites
    suites = [
        test_fuzzy_matcher(),
        test_topic_filter(),
        test_retrieval_system(),
        test_full_pipeline()
    ]
    
    # Calculate total
    total_passed = sum(s.passed for s in suites)
    total_failed = sum(s.failed for s in suites)
    total_tests = sum(s.total for s in suites)
    
    # Print overall summary
    print("\n" + "="*70)
    print("  OVERALL TEST SUMMARY")
    print("="*70)
    print(f"  Total Tests:  {total_tests}")
    print(f"  Passed:       {total_passed} ✓")
    print(f"  Failed:       {total_failed} ✗")
    print(f"  Success Rate: {(total_passed/total_tests*100):.1f}%")
    print("="*70 + "\n")
    
    if total_failed == 0:
        print("🎉 ALL TESTS PASSED! System ready for deployment.\n")
        return True
    else:
        print("⚠️  Some tests failed. Please review the results above.\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()