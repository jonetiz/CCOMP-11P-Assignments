#  _ _ _ _
# |\       \
# | \ _ _ _ \
# |  |       |
#  \ |   x   |
#   \|_ _ _ _|
# Dice Roller
# Written by Jon Etiz
# Created on 02SEP2022

# Used to generate a random integer
from random import randint
# Used to get and validate integers from user
from etizmodules import input_int
import math

num_dice = input_int("How many dice would you like to roll?", 1)
dice_sides = input_int("How many sides do the dice have?", 1)

a = []

for x in range(num_dice):
    a.append(randint(1, dice_sides))

for t in a:
    o = f""" _ _ _ _ 
|\       \\
| \ _ _ _ \\
|  |       |
 \ |{t}|
  \|_ _ _ _|"""

    print(o)