'''
Single-byte XOR cipher

The hex encoded string:

    1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score. 
'''

#frequencies taken from 
#http://www.macfreek.nl/memory/Letter_Distribution

import codecs
from collections import Counter
import re

FREQ = { 
    'a': 0.0653216702, 'b': 0.0125888074, 'c': 0.0223367596, 'd': 0.0328292310, 'e': 0.1026665037, 'f': 0.0198306716, 'g': 0.0162490441,
    'h': 0.0497856396, 'i': 0.0566844326, 'j': 0.0009752181, 'k': 0.0056096272, 'l': 0.0331754796, 'm': 0.0202656783, 'n': 0.0571201113,
    'o': 0.0615957725, 'p': 0.0150432428, 'q': 0.0008367550, 'r': 0.0498790855, 's': 0.0531700534, 't': 0.0751699827, 'u': 0.0227579536,
    'v': 0.0079611644, 'w': 0.0170389377, 'x': 0.0014092016, 'y': 0.0142766662, 'z': 0.0005128469, ' ': 0.1828846265,
    }

def char_xor(key=0,ct=0):
    output = ord(ct)^key
    return output

def main():
    hex_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    print(f"hex representation : {hex_str}")

    #put alphabet ascii ords into a list including space
    ascii_ord = list(range(ord('a'), ord('z')+1)) + list(range(ord('A'), ord('Z')+1))
    ascii_ord.append(ord(' '))

    # split hex_string in chunks of 2 to represent a single ascii char"
    chars= re.findall('..?',str(hex_str))
    ct_list = []
    for char in chars:
        ct_char = codecs.decode(char,"hex")
        ct_char = ct_char.decode('ascii')
        ct_list.append(ct_char)
    #    print(ord(ct_char))

    #extract the frequency score for each character in the ct and put them into a dictionary
    ct_counter= Counter(ct_list) 
    ct_frequencies= {}
    for char in ct_counter:
        ct_freq= ct_counter[char]/len(ct_counter)
        ct_frequencies[char]=ct_freq


    #get key associated to maximum value in FREQ
    alphabet_frequentest= max(FREQ, key=FREQ.get) 
    print(f'The frequentest character in english texts is   :"{alphabet_frequentest}"')

    #get key associated to maximum value in FREQ
    ct_frequentest= max(ct_frequencies, key=ct_frequencies.get)
    print(f'The frequentest character in the ct is          :"{ct_frequentest}"')
    #get key associated to maximum value in FREQ
    key = ord(alphabet_frequentest) ^ ord(ct_frequentest)
    print(f'It is likely that the encryption key is "{key}"')

    #xor every single character with the key
    most_likely_pt = [char_xor(key,item) for item in ct_list]

    #convert list in char and join it
    most_likely_pt = ''.join([chr(int(item)) for item in most_likely_pt])
    print(f'\nIt is likely that the pt is: \n"{most_likely_pt}"')

if __name__ == "__main__":
    main()
