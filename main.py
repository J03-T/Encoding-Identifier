#!/usr/bin/env python3
import sys
import string
import base64
try:
    import base45
    B45SUPPORT = True
except ImportError:
    B45SUPPORT = False

try:
    import base58
    B58SUPPORT = True
except ImportError:
    B58SUPPORT = False

try:
    import base62
    B62SUPPORT = True
except ImportError:
    B62SUPPORT = False

def is_hex(text: str) -> float:
    if any(map(lambda x: x not in string.hexdigits, text)):
        return 0
    return 1

def is_base64(text: str) -> float:
    b64_chars = string.digits + string.ascii_letters + '+/='
    if any(map(lambda x: x not in b64_chars, text)):
        return 0
    if text.find('=') not in [-1, len(text) - 1, len(text) - 2]:
        return 0.5
    try:
        base64.b64decode(text)
    except:
        return 0
    return 1

def is_base32(text: str):
    b32_chars = string.ascii_uppercase + "234567="
    if any(map(lambda x: x not in b32_chars, text)):
        return 0
    if text.find('=') not in [-1, len(text) - 1, len(text) - 2]:
        return 0.5
    try:
        base64.b32decode(text)
    except:
        return 0
    return 1

def is_binary(text: str):
    if any(map(lambda x: x not in '01 ', text)):
        return 0
    return 1

def is_decimal(text: str):
    if any(map(lambda x: x not in string.digits, text)):
        return 0
    return 1

def is_octal(text: str):
    if any(map(lambda x: x not in '01234567', text)):
        return 0
    return 1

def is_rot13(text: str):
    if any(map(lambda x: x not in string.printable, text)):
        return 0
    freqs = {l: text.count(l) for l in set(text) & set(string.ascii_letters)}
    if max(freqs.keys(), key=lambda k: freqs[k]) not in ['r', 'R', 'n', 'N', 'e', 'E', 'v', 'V', 'b', 'B', 'g', 'G']:
        return 0.5
    return 1

def is_rot47(text: str):
    if any(map(lambda x: x not in string.printable, text)):
        return 0
    freqs = {l: text.count(l) for l in set(text) & set(map(chr, range(33, 127)))}
    if max(freqs.keys(), key=lambda k: freqs[k]) not in ['6', 't', '2', 'p', '@', '~', 'C', '#', ':', 'x']:
        return 0.5
    return 1

def is_base45(text: str):
    if any(map(lambda x: x not in string.digits + string.ascii_uppercase + ' $%*+-./:', text)):
        return 0
    if B45SUPPORT:
        try:
            base45.b45decode(text)
        except:
            return 0
    return 1

def is_base58(text: str):
    if any(map(lambda x: x not in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', text)):
        return 0
    if B58SUPPORT:
        try:
            base58.b58decode(text)
        except:
            return 0
    return 1

def is_base62(text: str):
    if any(map(lambda x: x not in string.digits + string.ascii_letters, text)):
        return 0
    if B62SUPPORT:
        try:
            base62.decode(text)
        except:
            return 0
    return 1

def get_possible_encodings(text: str):
    encodings = {}
    encodings['binary'] = is_binary(text)
    encodings['octal'] = is_octal(text)
    encodings['decimal'] = is_decimal(text)
    encodings['hex'] = is_hex(text)
    encodings['rot13'] = is_rot13(text)
    encodings['rot47'] = is_rot47(text)
    encodings['base32'] = is_base32(text)
    encodings['base45'] = is_base45(text)
    encodings['base58'] = is_base58(text)
    encodings['base62'] = is_base62(text)
    encodings['base64'] = is_base64(text)
    likely = {}
    for e, l in encodings.items():
        if l > 0:
            likely[e] = l
    return likely

def print_dependency_warnings():
    if not B45SUPPORT:
        print("WARNING! The base45 module is not installed. Accuracy in identifying this format may be reduced. Please install it with 'pip install base45'!")
    if not B58SUPPORT:
        print("WARNING! The base58 module is not installed. Accuracy in identifying this format may be reduced. Please install it with 'pip install base58'!")
    if not B62SUPPORT:
        print("WARNING! The base62 module is not installed. Accuracy in identifying this format may be reduced. Please install it with 'pip install pybase62'!")
        
if __name__ == "__main__":
    print_dependency_warnings()
    if len(sys.argv) < 2:
        print(f"Usage: '{sys.argv[0]} <TEXT>'")
        exit(0)
    text = sys.argv[1]
    encodings = get_possible_encodings(text)
    print("Text is likely to be:")
    for encoding, likelihood in encodings.items():
        if likelihood == 1:
            print(encoding)
    print("Text may (unlikely) be:")
    for encoding, likelihood in encodings.items():
        if likelihood == 0.5:
            print(encoding)
