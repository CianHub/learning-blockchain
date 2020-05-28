""" Provides helper methods for hashing element """

import hashlib
import json


def hash_string_256(string):
    # creates a btye hash from the binary string
    # converst the byte hash to a string with hexdigest
    return hashlib.sha256(string).hexdigest()


def create_hashable_object(obj):
    return obj.__dict__.copy()


def create_hashable_obj_list(obj_list):
    return [create_hashable_object(obj) for obj in obj_list]


def create_hashable_block(block):
    hashable_block = create_hashable_object(block)
    hashable_block['transactions'] = create_hashable_obj_list(
        block.transactions)
    return hashable_block


def create_hashable_blockchain(blockchain):
    return [create_hashable_block(block) for block in blockchain]


def hash_block(block):
    # converts block dictionary to a binary string and encodes it
    # sort the dictionary by keys so it will always be in the same order

    return hash_string_256(json.dumps(create_hashable_block(block), sort_keys=True).encode())
