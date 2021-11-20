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

    hd=normalized_hamming(b"this is a test",b"wokka wokka!!!")
    print(f'the normalized binary-hamming distance is {hd}')
    best_keysizes={}

    #set the maximum number of iteration of the outer loop
    outer_end = round((len(chars)/2))+1

    for KEYSIZE in range(2,outer_end):
        best_keysizes[KEYSIZE]=0.0
        start = 1 
        #set the maximum number of iteration of the inner loop
        end = round(len(chars)/(KEYSIZE))
        count = 0 

        for step in range(start, end):
            if (step*KEYSIZE)+KEYSIZE > len(chars):
           #    print(f'breaking')
                break
            count+=1
            
            chunk1= chars[:KEYSIZE]
            chunk2= chars[step*KEYSIZE:step*KEYSIZE+KEYSIZE]


            print(f'compare: 0-{KEYSIZE} to :{step*KEYSIZE}:{step*KEYSIZE+KEYSIZE} steps: {count}')
            #add the value of the normalizzed hamming distance to the dictionary (which serves as a counter)
            best_keysizes[KEYSIZE] += normalized_hamming(chunk1,chunk2)

        #divide by the number of iterations of the innner loop to obtain the mean of the values
        best_keysizes[KEYSIZE]=best_keysizes[KEYSIZE]/count
        print(f'best keysize: {best_keysizes[KEYSIZE]} steps: {count}')

    #return the list of dictionary's keys sorted by their value
    sorted_kyesize = sorted(best_keysizes, key=best_keysizes.get)

    #print some values
    print(f'the best keysize is: {sorted_kyesize[0]} and its value is: {best_keysizes[sorted_kyesize[0]]}')
    print(f'the best keysize is: {sorted_kyesize[1]} and its value is: {best_keysizes[sorted_kyesize[1]]}')
    print(f'the best keysize is: {sorted_kyesize[2]} and its value is: {best_keysizes[sorted_kyesize[2]]}')
    print(f'the worst keysize is: {sorted_kyesize[-1]} and its value is: {best_keysizes[sorted_kyesize[-1]]}')
    print(f'the keysize of {3} and its value is: {best_keysizes[3]}')
    print(f'the keysize of {29} and its value is: {best_keysizes[29]}')

    #for the most likely 5 key-sizes, divide the text in chuks and attempt to find the key 
    for n in range(1,6):
        chunks = [string[i:i+n] for i in range(0, len(string), sorted_kyesize[n])]
        print(f'hex key: {}')
        

    #print the most promising 20 key-lenght candidates
    print(sorted_kyesize[:20])

    #for char in chars:
    #    ct_char = codecs.encode("ascii")
    #    ct_char = char.format(int(char,16))
        #ct_char = ct_char.decode('UTF8') #    ct_list.append(ct_char)
    #print(f'chars   :"{ct_list}"')
    #print(ord(ct_char))

if __name__ == "__main__":
    main()
