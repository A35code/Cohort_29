import re
text = "The cat sat on the mat."

# re.search finds the first ocurence of "cat" in the text
m = re.search(r"cat", text)
print("search returned", m)  # <re.Match object; span=(4, 7), match='cat'>

#r"cat" is a raw string literal
#it tells python to ignore escape sequences like \n, \t, etc."

if m:
    print("group 0 whole match: ", m.group(0))  # cat
    print("span: ", m.span())  # (4, 7)
    print("start, end indices: ", m.start(), m.end())  # 4 7


m = re.search(r"dog", text)
print("search for dog", m)

#re.match tries to find "The" only at the beginning of the text
m = re.match(r"The", text)
print("match returned", m)


print("fullmath entire string", re.fullmatch(r"mat", text))
print("fullmath entire string", re.fullmatch(r".*mat\.", text))
print("fullmath entire string", re.fullmatch(r"cat", "cat"))
print("fullmath entire string", re.fullmatch(r"cat", " a cat"))


#when you pass raw strings to re
#there are certain characters that have special meaning and act as commands
# . ^ $ * + ? { } [ ] \ | ( )  are some of them


#re.findall returns all non-overlapping matches of the pattern in the string as a list
print("findall('\\w+', 'one two three') -->", re.findall(r'\\w+', 'one two three'))


"""
. ---> any charater except new line
\d ---> digit (0-9)
\D ---> not a digit (0-9)
\w ---> word character (a-z, A-Z, 0-9, _)
$ ---> END OF A STRING
( ) ---> group
[ ] ---> matches characters in brackets
[^ ] ---> matches characters not in brackets

Quantifiers:
+ --->
? ---> 
* --->
{ } --->"""


#re.finditer returns all iterator yielding match objets for all non-overlapping matches of the pattern in the string

print(re.findall(r'[aeiou]', text))

print(re.findall(r'\d', "123 main street"))

print(re.findall(r'\d', "call 0803-345-6317 or +234 803 345 6314"))

print(re.findall(r'\d+', "call 0803-345-6317 or +234 803 345 6314"))

print(re.findall(r'\d*', "call 0803-345-6317 or +234 803 345 6314"))

print(re.findall(r'\w+', "Here's some text with-Hyphens."))

print(re.findall(r'\W+', "Here's some text with-Hyphens."))

#\b is a word boundary, which matches the position between a word charater and a non-word character i.e  it finds the exact word nothing behind or in front of it 
print(re.findall(r'\bthe\b', "the them over the"))

print(re.findall(r'[0-9]', "1234"))#finds numbers

print(re.findall(r'[^0-9]', "1234"))#finds non-numbers

print(re.findall(r'[a-zA-Z0-9]', text))

print(re.findall(r'ha+', "ha haaa HaHa"))

s = '<p>first</p><p>second</>'

print(re.search(r'<p>.*</p>', s).group())
print(re.search(r'<p>.*?</p>', s).group())