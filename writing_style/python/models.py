"""Building a model of writing style from a text file.
"""

import pathlib
import random
import math

alphabet = 'abcdefghijklmnopqrstuvwxyz '
alphabet_set = set([alphabet[i] for i in range(len(alphabet))])

def process_letters(text):
    text = text.replace('\n', ' ').lower()
    return ''.join( ( text[i] for i in range(len(text)) if text[i] in alphabet_set ) )

def raw_letters(text_file):
    text = process_letters(text_file.read_text())
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
    n = 0
    for k in f1:
        if k in f2:
            n = n + 1
            diff = f1[k] - f2[k]
            sq_dist = sq_dist + (diff * diff)
    return math.sqrt(sq_dist / n)

def log_odds(f1, f2):
    common_keys = [k for k in f1 if k in f2]
    return { k: math.log(f1[k]) - math.log(f2[k]) for k in common_keys }

s2c_log_odds = log_odds(shakespeare_frequencies, carroll_frequencies)

def log_score(log_odds, text):
    sum = 0.0
    for i in range(len(text)):
        sum += log_odds[text[i]]
    return sum / max(1, len(text))

def random_string(str, length):
    offset = random.randint(0, len(str) - length - 1)
    return str[offset:offset+length]

def random_shakespeare(length):
    return random_string(shakespeare, length)

def random_lewis_carroll(length):
    return random_string(lewis_carroll, length)

def test_text(text, margin=0.0):
    text = process_letters(text)
    s2c_score = log_score(s2c_log_odds, text)
    delta = abs(s2c_score)
    if delta >= margin:
        if s2c_score >= 0.0:
            print('%0.5f Shakespeare' % s2c_score)
        else:
            print('%0.5f Lewis Carroll' % s2c_score)
    else:
        #return '%0.5f ???' % delta
        pass
