import matplotlib.pyplot as plt
from dataset import generate_dataset
from login_checker import LoginChecker
from utils import timing_decorator
import random

@timing_decorator
def run_experiment(checker, dataset, num_lookups, search_type):
    """
    Runs a set of lookup experiments and times them.

    Args:
        checker (LoginChecker): An instance of the LoginChecker class.
        dataset (list): The dataset of usernames.
        num_lookups (int): The number of lookup operations to perform.
        search_type (str): The type of search to perform ('linear', 'binary', 'hash', 'bloom', 'cuckoo').
    """
    if search_type == "binary":
        dataset.sort()

    lookup_usernames = [random.choice(dataset) for _ in range(num_lookups)]
    lookup_usernames.extend([f"nonexistent_user_{i}" for i in range(num_lookups // 10)])

    if search_type == 'linear':
        for username in lookup_usernames:
            checker.linear_search(username)
    elif search_type == 'binary':
        for username in lookup_usernames:
            checker.binary_search(username)
    elif search_type == 'hash':
        for username in lookup_usernames:
            checker.hash_search(username)
    elif search_type == 'bloom':
        for username in lookup_usernames:
            checker.bloom_filter_check(username)
    elif search_type == 'cuckoo':
        for username in lookup_usernames:
            checker.cuckoo_filter_check(username)
    else:
        raise ValueError(f"Invalid search type: {search_type}")

def main():
    """
    Main function to run experiments and generate plots.
    """
    dataset_sizes = [1000, 5000, 10000, 50000, 100000]
    num_lookups = 1000
    search_types = ['linear', 'binary', 'hash', 'bloom', 'cuckoo']

    results = {}
    plt.figure(figsize=(12, 8))  # Create a larger figure for the combined plot

    for search_type in search_types:
        results[search_type] = []
        for size in dataset_sizes:
            print(f"Running {search_type} search with dataset size: {size}")
            dataset = generate_dataset(size)
            checker = LoginChecker(dataset=dataset, capacity=size, error_rate=0.01)
            elapsed_time = run_experiment(checker, dataset, num_lookups, search_type)
            results[search_type].append(elapsed_time)

        # Individual plot for each search type
        plt.figure(figsize=(8, 5))  # Create a separate figure for each algorithm
        plt.plot(dataset_sizes, results[search_type], label=search_type, marker='o')
        plt.xlabel("Dataset Size")
        plt.ylabel("Time (seconds)")
        plt.title(f"Runtime of {search_type.capitalize()} Search")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{search_type}_runtime.png")  # Save individual plot
        plt.close()  # Close the individual plot figure

        # Add to the combined plot
        plt.plot(dataset_sizes, results[search_type], label=search_type, marker='o')

    # Combined plot
    plt.xlabel("Dataset Size")
    plt.ylabel("Time (seconds)")
    plt.title("Runtime Comparison of Login Checking Algorithms")
    plt.legend()
    plt.grid(True)
    plt.savefig("combined_runtime_comparison.png")  # Save the combined plot
    plt.show()  # Show the combined plot (optional)

if __name__ == "__main__":
    main()