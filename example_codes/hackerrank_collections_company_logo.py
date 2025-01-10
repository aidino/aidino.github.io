#!/bin/python3

from collections import Counter

if __name__ == '__main__':
    s = input()
    ct = Counter(s) 
    sorted_ct = sorted(ct.items(), key=lambda item: (-item[1], item[0]))
    for chas, count in sorted_ct[:3]:
        print(f"{chas} {count}")
