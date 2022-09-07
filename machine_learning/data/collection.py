# Data Extraction Methodology for Space Placement in Sentences
#
# Extracts random-length paragraphs from English wikipedia pages,
# removes a random number of spaces from the paragraph, and places
# the edited data in the "input" field. Original data (with all spaces)
# is placed in the "output" field.

import wikipedia
from random import randint
import csv
from time import time
import re

# Get 100 random wikipedia page titles
keywords = wikipedia.random(pages=100)
# keywords = ["Python Programming Language", "The United States of America"] # Testing variables 

# Removes spaces and new lines
def remove_spaces(s: str):
    return s.replace(" ","").replace("\n","")

# Counter used for printing
counter = 0

# Write CSV file
with open(f'output/train_{int(time())}.csv', 'w+', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['input','output'])
    for keyword in keywords:
        data = ""
        try:
            # Attempt to get the summary of wikipedia page from keyword and remove all non-ASCII characters.
            data = re.sub(r'[^\x00-\x7f]', r'', wikipedia.summary(keyword))
        except:
            # If it throws an error, skip this iteration of for loop
            continue
        data_in = remove_spaces(data)
        data_out = data.replace("\n"," ")
        # Validate date is not empty
        if data_in != "":
            writer.writerow([data_in, data_out])
            print(f'[{counter}] Wrote "{keyword}" to CSV.')
            counter += 1