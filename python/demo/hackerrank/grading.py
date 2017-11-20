#!/bin/python3

import sys
import math

def solve(grades):
    # Complete this function
    for x in range(len(grades)):
        if grades[x] >= 38:
            if grades[x]%5 > 2:
                grades[x] = math.ceil(grades[x]/5) * 5
    return grades

n = int(input().strip())
grades = []
grades_i = 0
for grades_i in range(n):
   grades_t = int(input().strip())
   grades.append(grades_t)
result = solve(grades)
for x in grades:
    print(x)


