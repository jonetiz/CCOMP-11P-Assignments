# Project Euler Problem 348
# https://projecteuler.net/problem=348

def is_palindrome(num):
    return True if int(num) == int(str(num)[::-1]) else False
    
print(is_palindrome(1331))