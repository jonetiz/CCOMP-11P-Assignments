# Time Flies
# Written by Jon Etiz
# Created on 01SEP2022
# Generates a random number (100...8000), converts number into seconds, and outputs the calculation process.

# Used for RNG
from random import randint
# Used for time calculations
from dateutil.relativedelta import relativedelta
# Imports my methods
from etizmodules import *

# Generate a random integer between 100 and 8000
s = randint(100, 8000)

# Create relativedelta object from the number above as seconds.
t = relativedelta(seconds=s)

# Initialize explanation list which will be used with concat_numbers_as_string() to handle cases where there are 0 minutes with 1 hour and 34 seconds (for example)
explanation = []

if t.hours > 0:
    explanation.append(f"({t.hours}*3600)")

if t.minutes > 0:
    explanation.append(f"({t.minutes}*60)")

if t.seconds > 0:
    explanation.append(f"{t.seconds}")


print(f"{s} seconds is {relativedelta_to_string(t, 6)}.\nThis is because {concat_numbers_as_string(explanation)} = {s}.")