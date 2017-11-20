#!/bin/python3

import sys

def getRecord(s):
    # Complete this function
    best = worst = s[0]
    best_count = worst_count = 0
    for x in range(1,len(s)):
        if s[x]> best:
            best = s[x]
            best_count+=1
        if s[x]< worst:
            worst = s[x]
            worst_count += 1

    return [best_count, worst_count]

n = int(input().strip())
s = list(map(int, input().strip().split(' ')))
result = getRecord(s)
print (" ".join(map(str, result)))
