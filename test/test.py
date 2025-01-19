import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.login_checker import LoginChecker
from src.dataset import generate_dataset

def test_linear_search():
    dataset = generate_dataset(100)
    checker = LoginChecker(dataset=dataset)

    assert checker.linear_search(dataset[0]) == True
    assert checker.linear_search("nonexistent_user") == False

def test_binary_search():
    dataset = generate_dataset(100)
    checker = LoginChecker(dataset=dataset)

    assert checker.binary_search(dataset[0]) == True
    assert checker.binary_search("nonexistent_user") == False

def test_hash_search():
    dataset = generate_dataset(100)
    checker = LoginChecker(dataset=dataset)

    assert checker.hash_search(dataset[0]) == True
    assert checker.hash_search("nonexistent_user") == False

def test_bloom_filter():
    dataset = generate_dataset(100)
    checker = LoginChecker(dataset=dataset, capacity=100, error_rate=0.01)

    for i in range(5):
        assert checker.bloom_filter_check(dataset[i]) == True

    false_positives = 0
    for _ in range(100):
        if checker.bloom_filter_check("nonexistent_user" + str(_)):
            false_positives += 1
    assert false_positives <= 10  # Allow a small number of false positives

def test_cuckoo_filter():
    dataset = generate_dataset(100)
    checker = LoginChecker(dataset=dataset, capacity=100, error_rate=0.01)

    for i in range(5):
        assert checker.cuckoo_filter_check(dataset[i]) == True

    false_positives = 0
    for _ in range(100):
        if checker.cuckoo_filter_check("nonexistent_user" + str(_)):
            false_positives += 1
    assert false_positives <= 5 # Allow fewer false positives than Bloom filter

def run_tests():
    test_linear_search()
    test_binary_search()
    test_hash_search()
    test_bloom_filter()
    test_cuckoo_filter()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()