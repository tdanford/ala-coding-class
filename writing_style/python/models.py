"""Building a model of writing style from a text file.
"""

import pathlib
import random
import math

alphabet = 'abcdefghijklmnopqrstuvwxyz '
alphabet_set = set([alphabet[i] for i in range(len(alphabet))])

def raw_letters(text_file):
    text = text_file.read_text().replace('\n', ' ').lower()
    return ''.join( ( text[i] for i in range(len(text)) if text[i] in alphabet_set ) )

def read_shakespeare():
    base = pathlib.Path.home() / 'Desktop'
    shakespeare = base / 'complete-works-shakespeare.txt'
    return raw_letters(shakespeare)

def read_lewis_carroll():
    base = pathlib.Path.home() / 'Desktop'
    alice = base / 'alice-in-wonderland.txt'
    return raw_letters(alice)

def frequencies(text):
    total_count = 0
    counts = { alphabet[i]: 0 for i in range(len(alphabet)) }
    for i in range(len(text)):
        if text[i] in counts:
            counts[text[i]] = counts[text[i]] + 1
            total_count = total_count + 1
    return { alphabet[i]: counts[alphabet[i]] / max(1, total_count) for i in range(len(alphabet)) }

shakespeare = read_shakespeare()
lewis_carroll = read_lewis_carroll()
shakespeare_frequencies = frequencies(shakespeare)
carroll_frequencies = frequencies(lewis_carroll)

def freq_distance(f1, f2):
    sq_dist = 0.0
    for k in f1:
        if k in f2:
            diff = f1[k] - f2[k]
            sq_dist = sq_dist + (diff * diff)
    return math.sqrt(sq_dist)

def random_string(str, length):
    offset = random.randint(0, len(str) - length - 1)
    return str[offset:offset+length]

def random_shakespeare(length):
    return random_string(shakespeare, length)

def random_lewis_carroll(length):
    return random_string(lewis_carroll, length)

def test_text(text, margin=0.025):
    f = frequencies(text)
    shakes_dist = freq_distance(f, shakespeare_frequencies)
    lewis_dist = freq_distance(f, carroll_frequencies)
    delta = abs(shakes_dist - lewis_dist)
    if delta >= margin:
        if shakes_dist < lewis_dist:
            print('%0.5f Shakespeare' % delta)
        else:
            print('%0.5f Lewis Carroll' % delta)
    else:
        #return '%0.5f ???' % delta
        pass
