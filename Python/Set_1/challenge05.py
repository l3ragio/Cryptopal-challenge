'''
Implement repeating-key XOR

Here is the opening stanza of an important work of the English language:

    Burning 'em, if you ain't quick and nimble
    I go crazy when I hear a cymbal

Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on.

It should come out to:

    0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
    a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt your mail. Encrypt your password file. Your .sig file. Get a feel for it. I promise, we aren't wasting your time with this.
'''

#frequencies taken from 
#http://www.macfreek.nl/memory/Letter_Distribution

import codecs, binascii
from collections import Counter
import re

def char_xor(key=0,ct=0):
    output = ct^key
    return output

def main(string= b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'):

    print(f"hex representation : {string}")

    key=b'ICE'

    #split string and key in lists of characters
    n = 1
    keys = [key[i:i+n] for i in range(0, len(key), n)]
    print(f'hex key: {keys}')
    chars = [string[i:i+n] for i in range(0, len(string), n)]
    print(chars)

    xor_list = []
    i=0
    for char in chars:
        #for xor each char with the appropriate key character
        xor = char_xor(ord(keys[i%3]),ord(char)) 
        xor=format(xor, "x")
        xor=bytes(xor, 'utf-8')
        if len(xor)==1:
            xor=b'0'+xor
        xor_list.append(xor)

    xor_list= b''.join(xor_list)
    print(f'xorlist: {xor_list}')

if __name__ == "__main__":
    main()
