#!/bin/python3

import sys


n = int(input().strip())
unsorted = input().strip().split(' ')[:4]

def insertionSort(ar):
    for i in range(len(ar)):
        ar = update(ar,i)
        print(ar)
def update(ar, i):
    for x in range(i):
        if int(ar[x]) > int(ar[i]):
        	candicate = ar.pop(i)
            return ar[:x-1] + [ar[i]]+ ar[x:]
    return ar
insertionSort(unsorted)