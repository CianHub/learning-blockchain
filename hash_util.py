import hashlib
import json


def hash_string_256(string):
    # creates a btye hash from the binary string
    # converst the byte hash to a string with hexdigest
    return hashlib.sha256(string).hexdigest()


def create_hashable_block(block):
    return block.__dict__.copy()


def hash_block(block):
    # converts block dictionary to a binary string and encodes it
    # sort the dictionary by keys so it will always be in the same order
    hashable_block = create_hashable_block(block)
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
