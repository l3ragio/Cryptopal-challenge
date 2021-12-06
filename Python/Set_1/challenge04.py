'''
Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)
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

#def is_ascii(s):
#    return len(s) == len(s.encode())
    #return all(ord(c) < 128 for c in s)

def char_xor(key=0,ct=0):
    output = ord(ct)^key
    return output

def main():
    file4=""

    with open('4.txt', 'r') as file:
    # Reads all the file lines and put them into a list, then join the strings. 
        for line in file.readlines():
            hex_str = line
            #print(f'line: {hex_str}')

            #put alphabet ascii ords into a list including space
            ascii_ord = list(range(ord('a'), ord('z')+1)) + list(range(ord('A'), ord('Z')+1))
            ascii_ord.append(ord(' '))

            # split hex_string in chunks of 2 to represent a single ascii char"
            chars= re.findall('..?',str(hex_str))
            #print(f'chars   :"{chars}"')

            ct_list = []
            for char in chars:
                ct_char = codecs.decode(char,"hex")
                #ct_char = ct_char.decode('UTF8')
                ct_list.append(ct_char)
                #print(f'chars   :"{ct_char}"')
                #print(ord(ct_char))

            #extract the frequency score for each character in the ct and put them into a dictionary
            ct_counter= Counter(ct_list) 
            ct_frequencies= {}
            for char in ct_counter:
                ct_freq= ct_counter[char]/len(ct_counter)
                ct_frequencies[char]=ct_freq

            #get key associated to maximum value in FREQ
            alphabet_frequentest= max(FREQ, key=FREQ.get) 
            #print(f'The frequentest character in english texts is   :"{alphabet_frequentest}"')

            #get key associated to maximum value in FREQ
            ct_frequentest= max(ct_frequencies, key=ct_frequencies.get)
            #print(f'The frequentest character in the ct is          :"{ct_frequentest}"')
            #get key associated to maximum value in FREQ
            key = ord(alphabet_frequentest) ^ ord(ct_frequentest)
            #print(f'It is likely that the encryption key is "{key}"')

            #xor every single character with the key
            most_likely_pt = [char_xor(key,item) for item in ct_list]

            #convert list in char and join it
            most_likely_pt = ''.join([chr(int(item)) for item in most_likely_pt])

            #input('hey press enter')
            if most_likely_pt.isascii():
                print( most_likely_pt.encode('UTF8') )



if __name__ == "__main__":
    main()
