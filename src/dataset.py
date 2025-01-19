import random
import string

def generate_random_username(length=8):
    """
    Generates a random username.

    Args:
        length (int): The length of the username.

    Returns:
        str: A random username.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_dataset(num_usernames):
    """
    Generates a dataset of unique usernames.

    Args:
        num_usernames (int): The number of usernames to generate.

    Returns:
        list: A list of unique usernames.
    """
    usernames = set()
    while len(usernames) < num_usernames:
        usernames.add(generate_random_username())
    return list(usernames)