
import random

alphabet = 'abcdefghijklmnopqrstuvwxyz '

def random_offset():
    return random.randint(1, len(alphabet)-1)

def create_caesar_key():
    k = random_offset()
    def gen():
        while True:
            yield k
    return gen

def create_changing_caesar_key():
    starting_k = random_offset()
    shift = random_offset()
    def gen():
        current_k = starting_k
        while True:
            yield current_k
            current_k = (current_k + shift) % alphabet.length
    return gen

def encipher_letter(offset, letter):
    letter = letter.lower()
    idx = alphabet.find(letter)
    if idx >= 0:
        encoded_idx = (idx + key)  % len(alphabet)
        return alphabet[encoded_idx]
    else:
        return ''

def encipher_generator(key_gen, str_gen):
    return map(lambda p: encipher_letter(p[0], p[1]), zip(key_gen, str_gen))

def decipher(key, str_value):
    return encipher(map(lambda k: -k, key), str_value)

def encipher(key, str_value):
    string_gen = (str_value[i] for i in range(len(str_value)))
    return ''.join(encipher_generator(key, string_gen))
