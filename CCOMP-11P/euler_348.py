# Project Euler Problem 348
# https://projecteuler.net/problem=348

from time import time
from etizmodules import input_int

def is_palindrome(num):
    return num == int(str(num)[::-1])
    
desired = input_int("How many palindromes do you want the sum of?", 1)
found = {}
found2 = {}

start = time()
for i in range(1,100000):
    if len(found2) == desired:
        break
    i_squared = i**2
    for j in range(1,1000):
        if len(found2) == desired:
            break
        val = i_squared + j**3
        if is_palindrome(val):
            if val in found.keys():
                found[val].append((i, j))
                if len(found[val]) == 4:
                    found2[val] = found[val]
            else:
                found[val] = [(i, j)]
end = time()

output = 0

for val in found2:
    output += val

print(output)
print(f"{end - start} seconds elapsed.")