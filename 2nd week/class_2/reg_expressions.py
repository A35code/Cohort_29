import re

#re.search(pattern, string, flags=0)
#try to find the pattern at least once in the string. Returns a match object if found, else None.

#re.match(pattern, string, flags=0)
#try to find the pattern only at the beginning of the string. Returns a match object if found, else None.

#re.fullmatch(pattern, string, flags=0)
#try to find the pattern in the whole string. Returns a match object if found, else None.

#re.findall(pattern, string, flags=0)
#find all occurrences of the pattern in the string. Returns a list of strings.Returns an empty list if no match is found.

#re.finditer(pattern, string, flags=0)
#find all occurrences of the pattern in the string. Returns an iterator yielding match objects. Returns an empty iterator if no match is found.

#re.sub(pattern, repl, string, count=0, flags=0)
#Find all substrings where tehe pattern matches and replace them with a different string. Returns the modified string.

#re.compile(pattern, flags=0)
#Compile a regular expression pattern into a regular expression object, which can be used for matching using its methods.