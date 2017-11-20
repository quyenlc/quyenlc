#!/bin/python

import sys

# n = int(raw_input().strip())
# a = map(int,raw_input().strip().split(' '))
count = 0
content = open('/Users/quyen.le/git/infra-hn-common/user/quyen.le/python/demo/hackerrank/params.sort.txt','r')
lines = content.readlines()
n = int(lines[0])
a = map(int,lines[1].strip().split(' '))
content.close()
for i in range(n):
    for j in range(n-1-i):
        if (a[j]>a[j+1]):
            count+=1
            tmp = a[j]
            a[j]=a[j+1]
            a[j+1]=tmp
print "Array is sorted in {} swaps.".format(count)
print "First Element: {}".format(a[0])
print "Last Element: {}".format(a[n-1])

