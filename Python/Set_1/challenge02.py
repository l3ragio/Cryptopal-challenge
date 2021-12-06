'''
Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965

... should produce:

746865206b696420646f6e277420706c6179

'''

import codecs

def hextobin(x):
    return int(x, 16)

def main():

    hex_str = "1c0111001f010100061a024b53535009181c"
    xor_against = "686974207468652062756c6c277320657965"
    expected_result= "746865206b696420646f6e277420706c6179"

    print(f"Hex string                 : {hex_str}")
    print(f"String to be xored against : {xor_against}")
    print(f"Expected result            : {expected_result}")

    w = hextobin(hex_str)
    #w = w.decode('utf-8')
    print(f"Hex string binary representation        : {w}")

    z = hextobin(xor_against) 
    #z = z.decode('utf-8')
    print(f"Xor string binary representation        : {z}")

    xor= w^z
    xor = format(xor, 'x')

    print(f"result                     : {xor}")


if __name__ == "__main__":
    main()
