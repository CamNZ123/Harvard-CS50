#!/usr/bin/env python3

import cs50
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage python caesar.py k")
    else:
        s = str(input('plaintext: '))
        i = int(sys.argv[1]) % 26
        c = ""
        print("ciphertext: ", end = "")
        count = 0
        for x in range(len(s)):
            temp = chr(ord(s[x]) + i)
            if ((ord(s[x]) > 64 and ord(s[x]) < 91) or (ord(s[x]) > 96 and ord(s[x]) < 123)):
                if not temp.isalpha():
                    c = chr(ord(s[x]) - (26 - i))
                else:
                    c = chr(ord(s[x]) + i)
                
                print(c, end="")
                
        print()
        


main()