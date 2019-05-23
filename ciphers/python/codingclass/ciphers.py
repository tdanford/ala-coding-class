
import random

def create_key():
    return random.randint(1, len(alphabet)-1)

alphabet = 'abcdefghijklmnopqrstuvwxyz '

def encode_generator(key, generator):
    for letter in generator:
        letter = letter.lower()
        idx = alphabet.find(letter)
        if idx >= 0:
            encoded_idx = (idx + key)  % len(alphabet)
            yield key, alphabet[encoded_idx]

def decode(key, str_value):
    return encode(-key, str_value)

def encode(key, str_value):
    return ''.join(encode_generator(key, (str_value[i] for i in range(len(str_value)))))
