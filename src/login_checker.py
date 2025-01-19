from utils import simple_hash, mmh3_hash
import math
import random

class LoginChecker:
    def __init__(self, dataset=None, capacity=None, error_rate=0.001):
        """
        Initializes data structures for login checking algorithms.

        Args:
            dataset (list, optional): Pre-existing dataset of usernames. Defaults to None.
            capacity (int, optional): Estimated capacity for Bloom/Cuckoo filters. Defaults to None.
            error_rate (float, optional): Desired error rate for Bloom filter. Defaults to 0.001.
        """
        if dataset:
            self.dataset = dataset
            self.dataset_set = set(dataset)  # For hashing
            self.dataset.sort()  # For binary search

            # Bloom filter parameters
            self.capacity = len(dataset)
            self.error_rate = error_rate
            
            # Corrected the order here:
            self.bit_array_size = self._calculate_bit_array_size() # Calculate bit array size first
            self.num_hashes = self._calculate_num_hashes() # Then calculate the number of hashes
            
            self.bit_array = [0] * self.bit_array_size

            # Cuckoo filter parameters
            self.bucket_size = 4
            self.fingerprint_size = 2  # Adjust as needed
            self.max_displacements = 500 # Max kickout
            self.cuckoo_table = [([None] * self.bucket_size) for _ in range(self.capacity)]

            # Populate filters using the dataset
            for item in dataset:
                self._add_to_bloom_filter(item)
                self._insert_to_cuckoo_filter(item)
        else:
            self.dataset = []
            self.dataset_set = set()

            # Initialize filters with capacity and error_rate
            self.capacity = capacity
            self.error_rate = error_rate
            
            # Corrected the order here:
            self.bit_array_size = self._calculate_bit_array_size()
            self.num_hashes = self._calculate_num_hashes()
            
            self.bit_array = [0] * self.bit_array_size

            self.bucket_size = 4
            self.fingerprint_size = 2
            self.max_displacements = 500
            self.cuckoo_table = [([None] * self.bucket_size) for _ in range(self.capacity)]

    def linear_search(self, username):
        """
        Checks if a username exists using linear search.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        for item in self.dataset:
            if item == username:
                return True
        return False

    def binary_search(self, username):
        """
        Checks if a username exists using binary search.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        low = 0
        high = len(self.dataset) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.dataset[mid] == username:
                return True
            elif self.dataset[mid] < username:
                low = mid + 1
            else:
                high = mid - 1
        return False

    def hash_search(self, username):
        """
        Checks if a username exists using a hash set.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        return username in self.dataset_set
    
    def _calculate_bit_array_size(self):
        """
        Calculates the optimal size of the bit array for a Bloom filter.

        Returns:
            int: The size of the bit array.
        """
        m = - (self.capacity * math.log(self.error_rate)) / (math.log(2) ** 2)
        return int(m)

    def _calculate_num_hashes(self):
        """
        Calculates the optimal number of hash functions for a Bloom filter.

        Returns:
            int: The number of hash functions.
        """
        k = (self.bit_array_size / self.capacity) * math.log(2)
        return int(k)
    
    def _add_to_bloom_filter(self, username):
        """
        Adds a username to the Bloom filter.

        Args:
            username (str): The username to add.
        """
        for i in range(self.num_hashes):
            index = mmh3_hash(username, self.bit_array_size, seed=i)
            self.bit_array[index] = 1

    def bloom_filter_check(self, username):
        """
        Checks if a username might exist in the Bloom filter.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username might exist, False if it definitely does not.
        """
        for i in range(self.num_hashes):
            index = mmh3_hash(username, self.bit_array_size, seed=i)
            if self.bit_array[index] == 0:
                return False
        return True
    
    def _get_fingerprint(self, item):
        """
        Generates a fingerprint for an item.

        Args:
            item (str): The item for which to generate a fingerprint.

        Returns:
            int: The fingerprint of the item.
        """
        hash_value = mmh3_hash(item, 2**(self.fingerprint_size * 8))
        return hash_value & ((1 << (self.fingerprint_size * 8)) - 1)

    def _insert_to_cuckoo_filter(self, item):
        """
        Inserts an item into the Cuckoo filter.

        Args:
            item (str): The item to insert.
        """
        f = self._get_fingerprint(item)
        i1 = simple_hash(item, self.capacity)
        i2 = (i1 ^ simple_hash(str(f), self.capacity)) % self.capacity

        for _ in range(self.max_displacements):
            for index in [i1, i2]:
                if 0 <= index < len(self.cuckoo_table):  # Check index bounds
                    for j in range(self.bucket_size):
                        if self.cuckoo_table[index][j] is None:
                            self.cuckoo_table[index][j] = f
                            return

            # If no empty slot, randomly kick out an item
            index = random.choice([i1, i2])
            if 0 <= index < len(self.cuckoo_table):  # Check index bounds
                j = random.randrange(self.bucket_size)
                f, self.cuckoo_table[index][j] = self.cuckoo_table[index][j], f
                i1 = index
                i2 = (i1 ^ simple_hash(str(f), self.capacity)) % self.capacity

        # If max displacements reached, filter is considered full
        raise Exception("Cuckoo filter is full")

    def cuckoo_filter_check(self, item):
        """
        Checks if an item might exist in the Cuckoo filter.

        Args:
            item (str): The item to check.

        Returns:
            bool: True if the item might exist, False if it definitely does not.
        """
        f = self._get_fingerprint(item)
        i1 = simple_hash(item, self.capacity)
        i2 = (i1 ^ simple_hash(str(f), self.capacity)) % self.capacity

        for index in [i1, i2]:
            if 0 <= index < len(self.cuckoo_table):  # Check index bounds
                for j in range(self.bucket_size):
                    if self.cuckoo_table[index][j] == f:
                        return True
        return False
