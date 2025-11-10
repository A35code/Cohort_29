import re

urls = '''
https://www.google.com
http://coreyms.com.ng
https://youtube.com
https://www.nasa.gov
It should not detect this www.test.com
'''

pattern = re.compile(r'https?://(www\.)?[a-zA-Z]+\.[a-zA-z.:]+')

matches = pattern.finditer(urls)
for match in matches:
  print(match)
# subbed_urls = pattern.sub(r'\2\3', urls)

# print(subbed_urls)

# matches = pattern.finditer(urls)

# for match in matches:
#     print(match.group(3))
