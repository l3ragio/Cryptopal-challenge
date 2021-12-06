'''
There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.and    Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:

this is a test

and

wokka wokka!!!

is 37. Make sure your code agrees before you proceed.
For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
Solve each block as if it was single-character XOR. You already have code to do this.
For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.

This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.
No, that's not a mistake.

We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors in this text. In particular: the "wokka wokka!!!" edit distance really is 37.
'''

#frequencies taken from 
#http://www.macfreek.nl/memory/Letter_Distribution
#requires: 
#pip install hexhamming

import codecs 
import base64
from hexhamming import hamming_distance_bytes
from langdetect import detect
from challenge03 import ch3
from collections import defaultdict


def max_index(list):
    return len(list)-1

def char_xor(key=0,ct=0):
    output = ord(ct)^key
    return output

def normalized_hamming(s1,s2):
    return binary_hamming(s1, s2)/len(s2)

#Return the binary Hamming distance between equal-length sequences.
def binary_hamming(s1, s2):
    if len(s1) != len(s2):
        print('return the hamming distance between the first '+ str(len(s2))+' bytes')
        return hamming_distance_bytes(s1[:len(s2)],s2)
    return hamming_distance_bytes(s1,s2)

def find_key_sizes(chars, max_ks = 1024, start_key_size = 2):
    best_keysizes= {}

    #set the maximum number of iteration of the outer loop
    outer_end = round((len(chars)/2))+1

    # bound the maximum number of iterations to be the max key-length we want to consider
    if outer_end > max_ks:
        outer_end = max_ks

    #initialize list that will contain the chunks to be sorted
    chunks =  {} 

    for KEYSIZE in range(start_key_size,outer_end):
        best_keysizes[KEYSIZE]=0.0
        start = 1 
        #set the maximum number of iteration of the inner loop
        end = round(len(chars)/(KEYSIZE))
        count = 0 

        #initialize chunks ks list and append the first chunk    
        chunks[KEYSIZE]= [] 
        #print(chunks[KEYSIZE])
        chunk1= chars[:KEYSIZE]
        chunks[KEYSIZE].append(chunk1)
        for step in range(start, end):
            if (step*KEYSIZE)+KEYSIZE > len(chars):
           #    print(f'breaking')
                break
            count+=1
            
            chunk2= chars[step*KEYSIZE:(step+1)*KEYSIZE]

            chunks[KEYSIZE].append(chunk2)

            #print(f'compare: 0-{KEYSIZE} to :{step*KEYSIZE}:{(step+1)*KEYSIZE} steps: {count}')
            #add the value of the normalizzed hamming distance to the dictionary (which serves as a counter)
            best_keysizes[KEYSIZE] += normalized_hamming(chunk1,chunk2)

        #divide by the number of iterations of the innner loop to obtain the mean of the values
        best_keysizes[KEYSIZE]=best_keysizes[KEYSIZE]/count
        #print(f'best keysize: {best_keysizes[KEYSIZE]} steps: {count}')

    #return the list of dictionary's keys sorted by their value
    sorted_keysize = sorted(best_keysizes, key=best_keysizes.get)
    return sorted_keysize,chunks 
    

def main():
    file6=""
    with open('6.txt', 'r') as file:
        file6 = file.read()
    hex_str = file6
    print(f'file: {hex_str}')
    b64_str=base64.b64decode(hex_str)
    print(f'file: {b64_str}')

    #b64_str = b=b'0b3c3b2720272e696e2c246569202f6930263c692820276e3d69383c202a226928272d692720242b252c4300692e26692a3b283330693e212c27690069212c283b6928692a30242b2825'
    chars = b64_str

    #hd=normalized_hamming(b"this is a test",b"wokka wokka!!!")
    #print(f'the normalized binary-hamming distance is {hd}')
    sorted_keysize, chunks = find_key_sizes(chars)

    num=6
    #for the most likely "num" key-sizes, divide the text in chuks and attempt to find the key 
    start_key_size = 2

    #put in a new list the first num keysizes that contains just the keys we want to evaluate
    num_keysizes= sorted_keysize[:num]
    
    block_chunks= {}
    for n in num_keysizes:
        block_chunks[n] = { k : [] for k in range(n) }
        for i in range(len(chunks[n])):
            for j in range(n):
                block_chunks[n][j].append(chr(chunks[n][i][j]))

    print(f'block_chunks: {block_chunks[29]}')

#        for i in range(sorted_keysize[n]):
    #    find the most frequent character
    keys= {}
    for n in num_keysizes:
        keys[n] =[] 
        print(f'keys[{n}]: { keys[n]}')
        for i in range(len(block_chunks[n])):
            keys[n].append(ch3(block_chunks[n][i]))
            print(f'[{n}][{i}]: keys {keys[n][i]} -- block_chunks{block_chunks[n][i]}')

    print(f'keys: { keys[29]}')
    
    print(f'keys: { keys[29]}')

    
    #GOT KEYS FOR EACH BLOCK SIZE
    #now decrypt the chunks
    most_likely_pt ={}
    for n in num_keysizes:
        most_likely_pt[n] = []
        for i in range(len(chars)):
            most_likely_pt[n].append(chr(char_xor(keys[n][i%n],chr(chars[i]))))
        #most_likely_pt[n] = ''.join([chr(int(item)) for item in most_likely_pt[n]])


    #print the most promising 20 key-lenght candidates
    print(most_likely_pt[n])
    #GOT IT BUT SOME KEY VALUES ARE WRONG!

if __name__ == "__main__":
    main()
