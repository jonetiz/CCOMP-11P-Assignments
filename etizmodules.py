# Modules used by Jonathan Etiz for CCOMP-11P

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

def concat_numbers_as_string(l):
    '''
    Returns a concatenated list as a single string with plus signs.\n
    Examples:\n
    `['a','b','c','d']` => a + b + c + d\n
    `['a','b','c']` => a + b + c\n
    `['a','b']` => a + b\n
    `['a']` => a
    '''
    if len(l) == 1:
        # If l is only one element long, return the element.
        return f"{str(l[0])}"
    else:
        # If l is 2 or more elements long, return the concatenated list with + signs in between.
        o = ""
        for i, s in enumerate(l):
            if i == len(l) - 1:
                # If this iteration is the last element of l, just add the thing.
                o += f"{str(s)}"
            else:
                # If this iteration is not the last element of l, add plus signs.
                o += f"{str(s)} + "
        return o


# Takes a relativedelta and converts to a readable string.
def relativedelta_to_string(r, p=0):
    '''
    Converts a relativedelta into a string representation of "x years, y months, z days, y hours, i hours, j minutes, k seconds, and l microseconds".\n
    `p` is the precision variable. p=0 (default) will return the delta down to years, while 2 will return the delta down to days. Maxmimum value of p is 6.\n
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
    d = [r.years, r.months, r.days, r.hours,
         r.minutes, r.seconds, r.microseconds]
    out = []

    if d[0] == 0 and d[1] == 0 and d[2] == 0 and p <= 2:
        # If r has no years, months, or days, it must be today.
        return "today"

    if d[0] == 0 and d[1] == 0 and d[2] == 1 and p <= 2:
        # If r has no years, months, and there is only one day, it must be tomorrow.
        return "tomorrow"

    for v in range(p+1):
        if abs(d[v]) > 0:
            out.append(f"{abs(d[v])} ")
            if v == 0:
                out[-1] += "year"
            elif v == 1:
                out[-1] += "month"
            elif v == 2:
                out[-1] += "day"
            elif v == 3:
                out[-1] += "hour"
            elif v == 4:
                out[-1] += "minute"
            elif v == 5:
                out[-1] += "second"
            elif v == 6:
                out[-1] += "microsecond"

            out[-1] += "s" if abs(d[v]) > 1 else ""

    # if abs(y) > 0 and p >= 0:
    #     # If |y| > 0, add y year(s) to the list out.
    #     out.append(f"{abs(y)} year")
    #     out[-1] += "s" if abs(y) > 1 else ""

    # if abs(m) > 0 and p >= 1:
    #     # If |m| > 0, add m month(s) to the list out.
    #     out.append(f"{abs(m)} month")
    #     out[-1] += "s" if abs(m) > 1 else ""

    # if abs(d) > 0 and p >= 2:
    #     # If |d| > 0, add d day(s) to the list out.
    #     out.append(f"{abs(d)} day")
    #     out[-1] += "s" if abs(d) > 1 else ""

    # if abs(hh) > 0 and p >= 3:
    #     # If |hh| > 0, add hh hour(s) to the list out.
    #     out.append(f"{abs(hh)} hour")
    #     out[-1] += "s" if abs(hh) > 1 else ""

    # if abs(mm) > 0 and p >= 4:
    #     # If |mm| > 0, add mm minute(s) to the list out.
    #     out.append(f"{abs(mm)} minute")
    #     out[-1] += "s" if abs(mm) > 1 else ""

    # if abs(ss) > 0 and p >= 5:
    #     # If |ss| > 0, add ss second(s) to the list out.
    #     out.append(f"{abs(ss)} second")
    #     out[-1] += "s" if abs(ss) > 1 else ""

    # if abs(us) > 0 and p >= 6:
    #     # If |us| > 0, add us microsecond(s) to the list out.
    #     out.append(f"{abs(us)} microsecond")
    #     out[-1] += "s" if abs(us) > 1 else ""

    # Pass the list out to concat_with_punctuation and return the concatenated list. If r is in the past, add " ago" to the end.
    return f"{concat_with_punctuation(out)} ago" if d[0] <= 0 and d[1] <= 0 and d[2] <= 0 and p <= 2 else concat_with_punctuation(
        out)
