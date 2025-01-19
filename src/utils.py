import time
import random

def timing_decorator(func):
    """
    Decorator to measure the execution time of a function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds")
        return elapsed_time  # Return the elapsed time
    return wrapper

def simple_hash(s, m):
    """
    A very basic hash function for demonstration.

    Args:
        s (str): The string to hash.
        m (int): The size of the hash table or bit array.

    Returns:
        int: The hash value (an index between 0 and m-1).
    """
    hash_val = 0
    for char in s:
        hash_val = (hash_val * 31 + ord(char)) % m  # Using a prime multiplier
    return hash_val

def mmh3_hash(s, m, seed=0):
    """
    A basic implementation of MurmurHash3 (32-bit version) for demonstration.

    Args:
        s (str): The string to hash.
        m (int): The size of the hash table or bit array.
        seed (int): Seed for the hash function

    Returns:
        int: The hash value (an index between 0 and m-1).
    """
    def fmix32(h):
        h ^= h >> 16
        h = (h * 0x85ebca6b) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * 0xc2b2ae35) & 0xFFFFFFFF
        h ^= h >> 16
        return h

    length = len(s)
    n_blocks = int(length / 4)

    h1 = seed

    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # body
    for block_start in range(0, n_blocks * 4, 4):
        # little endian
        k1 = ord(s[block_start + 3]) << 24 | \
            ord(s[block_start + 2]) << 16 | \
            ord(s[block_start + 1]) << 8 | \
            ord(s[block_start + 0])

        k1 = (c1 * k1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  # inlined ROTL32
        k1 = (c2 * k1) & 0xFFFFFFFF

        h1 ^= k1
        h1 = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF  # inlined ROTL32
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    # tail
    tail_index = n_blocks * 4
    k1 = 0
    tail_size = length & 3

    if tail_size >= 3:
        k1 ^= ord(s[tail_index + 2]) << 16
    if tail_size >= 2:
        k1 ^= ord(s[tail_index + 1]) << 8
    if tail_size >= 1:
        k1 ^= ord(s[tail_index + 0])

    if tail_size > 0:
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  # inlined ROTL32
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    # finalization
    unsigned_val = fmix32(h1 ^ length)
    return unsigned_val % m