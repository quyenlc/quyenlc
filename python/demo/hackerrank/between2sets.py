#!/bin/python3

import sys


n,m = input().strip().split(' ')
n,m = [int(n),int(m)]
a = [int(a_temp) for a_temp in input().strip().split(' ')]
b = [int(b_temp) for b_temp in input().strip().split(' ')]

def isFactor(candicate, afp):
	for x in afp:
		if candicate%x != 0:
			return False
	return True

def isSubFactor(candicate, afp):
	for x in afp:
		if x%candicate != 0:
			return False
	return True

count = 0
for x in range(max(a),min(b)+1):
	if isFactor(x,a) and isSubFactor(x,b):
		count +=1
print(count)
