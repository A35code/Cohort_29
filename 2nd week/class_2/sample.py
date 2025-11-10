import re

text_search ="""
Mr. Skar
Mr Smith
Ms Davies
Mrs Robinson
Mr. T"""

#pattern = re.compile(r"M(r|s|rs)\.?\s[A-Z][a-z]*")

#matches = pattern.finditer(text_search)
#print(matches)

pattern = re.compile(r'[89]00.\d{3}.\d{4}')

with open("data.txt", "r") as f:
    contents = f.read()
    matches = pattern.finditer(contents)
    for match in matches:
        print(match)