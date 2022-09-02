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


# Get an integer based on user input and check that it is integer
def input_int(question, min=None, max=None):
    '''
    Returns a user-inputted integer.\n
    `question` is the input prompt.\n
    `min` is an optional minimum and `max` is an optional maximum value. If unset, they will not be checked.
    '''

    # Ask the question
    check = input(f"\n{question} ({min}...{max})\n")
    try:
        # Try casting check to integer
        int(check)
    except:
        # If typecast fails, prompt user for a new integer using question_fail.
        print(f"{check} is not a valid integer.")
        return input_int(f"{question}", min, max)
    else:
        # If typecast succeeds, check that the user input falls between specified min and max.
        if max is not None and int(check) > int(max):
            # If max is set and the checked value is greater than max, return another input_int informing user that their input exceeds max.
            print(f"The value must be between {min} and {max}.\n")
            return input_int(question, min, max)
        elif min is not None and int(check) < int(min):
            # If min is set and the checked value is less than min, return another input_int informing user that their input is less than min.
            print(f"The value must be between {min} and {max}.\n")
            return input_int(question, min, max)
        else:
            # Assuming the checked value is within the specified minimum and maximum, return the value as an integer.
            return int(check)


# Returns a number in ordinal form (ie. make_ordinal(1) => "1st")
def make_ordinal(n):
    '''
    Converts an integer into its ordinal representation.\n
    Examples:\n
    `1` => 1st\n
    `202` => 202nd\n
    `304` => 304th\n
    `495` => 495th
    '''

    # Array of suffixes that will be used. Two 'th' entries to include 0th and 4th ... 9th
    suffixes = ['th', 'st', 'nd', 'rd', 'th']

    try:
        # Check that n is castable to int
        n = int(n)
    except:
        # If there is an error, print the below message.
        print("Variable passed to make_ordinal is not an integer.")
    else:
        # If n is castable to int, check if n is a number ending in 11, 12, or 13
        if 11 <= (n % 100) <= 13:
            # If n ends in 11, 12, or 13, force the suffix "th" (eg. 1013th or 192511th)
            suffix = suffixes[0]
        else:
            # If n does not end in 11, 12, or 13, assign one of the suffixes from the array above based on the number of the final digit of the integer.
            suffix = suffixes[min(n % 10, 4)]
        return str(n) + suffix


# Concatenate a list with punctuation (['apple','orange','banana'] => "apple, orange, and banana")
def concat_with_punctuation(l):
    '''
    Returns a concatenated list as a single string with proper puncuation and the word "and".\n
    Examples:\n
    `['a','b','c','d']` => a, b, c, and d\n
    `['a','b','c']` => a, b, and c\n
    `['a','b']` => a and b\n
    `['a']` => a
    '''
    if len(l) == 1:
        # If l is only one element long, return the element.
        return f"{str(l[0])}"
    elif len(l) == 2:
        # If l is only two elements long, return the two elements separated with " and ".
        return f"{str(l[0])} and {str(l[1])}"
    else:
        # If l is 3 or more elements long, return the concatenated list with punctuation and " and " at the end.
        o = ""
        for i, s in enumerate(l):
            if i == len(l) - 1:
                # If this iteration is the last element of l, add the " and "
                o += f"and {str(s)}"
            else:
                # If this iteration is not the last element of l, add a comma and space.
                o += f"{str(s)}, "
        return o


# Takes a relativedelta and converts to a readable string.
def relativedelta_to_string(r):
    '''
    Converts a relativedelta into a string representation of "x years, y months, and z days". If there are no months, they are omitted from the string.\n
    Examples:\n
    `[years=+3,months=+5,days=+2]` => 3 years, 5 months, and 2 days\n
    `[months=+5,days=+2]` => 5 months and 2 days\n
    `[years=+3,days=+2]` => 3 years and 2 days\n
    `[days=+2]` => 2 days
    '''
    # Ensure the passed parameter is a relativedelta.
    if not isinstance(r, relativedelta):
        return "Parameter r passed to relativedelta_to_string(r) is not a relativedelta."

    # Not applying absolute value here so we can check if r is in the past.
    y = r.years
    m = r.months
    d = r.days
    out = []

    if y == 0 and m == 0 and d == 0:
        # If r has no years, months, or days, it must be today.
        return "today"

    if y == 0 and m == 0 and d == 1:
        # If r has no years, months, and there is only one day, it must be tomorrow.
        return "tomorrow"

    if abs(y) > 0:
        # If |y| > 0, add y year(s) to the list out.
        out.append(f"{abs(y)} year")
        out[-1] += "s" if abs(y) > 1 else ""

    if abs(m) > 0:
        # If |m| > 0, add m month(s) to the list out.
        out.append(f"{abs(m)} month")
        out[-1] += "s" if abs(m) > 1 else ""

    if abs(d) > 0:
        # If |d| > 0, add d day(s) to the list out.
        out.append(f"{abs(d)} day")
        out[-1] += "s" if abs(d) > 1 else ""

    # Pass the list out to concat_with_punctuation and return the concatenated list. If r is in the past, add " ago" to the end.
    return f"{concat_with_punctuation(out)} ago" if y <= 0 and m <= 0 and d <= 0 else concat_with_punctuation(
        out)


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
delta_formatted = relativedelta_to_string(delta)

# Format delta_ago as a user-friendly string.
delta_ago_formatted = relativedelta_to_string(delta_ago)

# Print final result
print(
    f"\nYou were born {delta_ago_formatted}.\nYour {make_ordinal(age+1)} birthday is {'in ' if delta_formatted is not 'tomorrow' else ''}{delta_formatted}."
)
