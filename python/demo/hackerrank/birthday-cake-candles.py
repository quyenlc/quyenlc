#!/bin/python3

import sys


n = int(input().strip())
height = [int(height_temp) for height_temp in input().strip().split(' ')]
visible = 0
max_heigh = 0
for i in range(len(height)):
    cur_h = height[i]
    if cur_h > max_heigh:
    	max_heigh = cur_h
    	visible =1
    elif cur_h == max_heigh:
    	visible+=1
print(visible)    	
