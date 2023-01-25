# Question and Answer
# Written by Jon Etiz
# Created on 30AUG2022
# Ever forget how old you are? This utility returns your age and how long until your next birthday.

# Imports date which is used for date objects and logic thereof.
from datetime import date
# Imports floor which is used to get the age.
from math import floor
# Imports monthrange which is used to calculate the number of days in a month.
from calendar import monthrange
# Imports relativedelta which is used to get the number of months in delta.
from dateutil.relativedelta import relativedelta
# Imports my modules
from etizmodules import *


# Instantiate date object for today.
today = date.today()

# Use input_int to get year of birth. No minimum year, maximum of current year.
yob = input_int("What year were you born in?", 1, today.year)

# Use input_int to get month of birth. Must be numeric between 1 and 12.
mob = input_int(
    "What month were you born in?", 1, 12 if yob != today.year else today.month
)  # Ensure that nobody born next month is able to break the laws of time and space to use this program today.

# Calculate the number of days in the specified month of the specified year.
days_allowed = monthrange(yob, mob)

# Use input_int to get day of birth. Must be numeric between 1 and index 1 of the returned days_allowed.
dob = input_int(
    f"What day were you born on?", 1,
    days_allowed[1] if yob != today.year or mob != today.month else today.day
)  # Ensure that nobody born tomorrow is able to break the laws of time and space to use this program today.

# Instantiate date object for the date of birth.
dob_full = date(yob, mob, dob)

# Get the user's age in ordinal form based on the previous inputs.
age = floor((today - dob_full).days / 365)

# Calculate number of days until birthday. Handles leap year edge case.
if yob % 4 == 0 and mob == 2 and dob == 29:
    delta = relativedelta(date(today.year, 2, 28), today)
else:
    delta = relativedelta(date(today.year, mob, dob), today)

# How long ago the user was born.
delta_ago = relativedelta(dob_full, today)

# Handle cases where the birthday has passed or is today by checking next year.
if delta.days <= 0 and delta.months <= 0 and delta.years <= 0:
    if yob % 4 == 0 and mob == 2 and dob == 29:
        delta = relativedelta(date(today.year + 1, 2, 28), today)
    else:
        delta = relativedelta(date(today.year + 1, mob, dob), today)

# Format delta as a user-friendly string.
delta_formatted = relativedelta_to_string(delta, 2)

# Format delta_ago as a user-friendly string.
delta_ago_formatted = relativedelta_to_string(delta_ago, 2)

# Print final result
print(
    f"\nYou were born {delta_ago_formatted}.\nYour {make_ordinal(age+1)} birthday is {'in ' if delta_formatted != 'tomorrow' else ''}{delta_formatted}."
)
