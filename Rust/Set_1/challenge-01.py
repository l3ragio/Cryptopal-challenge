'''
Convert hex to base64

The string:

49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

Should produce:

SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

So go ahead and make that happen. You'll need to use this code for the rest of the exercises.
Cryptopals Rule

Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.
'''

import codecs

def hextob64(x, encoding1, encoding2):
    return codecs.encode(codecs.decode(x, encoding1), encoding2)

def main():
    hex_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    b64_str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

    print(f"Input         : {hex_str}")
    print(f"Desired output: {b64_str}")

    w = hextob64(hex_str, "hex", "base64")
    w = w.decode('utf-8')
    print(f"Output        : {w}")

    z = codecs.decode(hex_str,"hex") 
    z = z.decode('utf-8')
    print(f"Decoded input : {z}")


if __name__ == "__main__":
    main()
