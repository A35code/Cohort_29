import re


m = re.findall(r'(\w+)@(\w+)\.(\w+)', 'user@example.com')
print(m) #caputing each word in "user@example.com"
#@ is not in the bracket "(\w+) so it is not picked"

text = "This is a test. That that should be fixed."
print(re.findall(r'that', text, flags=re.IGNORECASE))
print(re.findall(r'\b(\w+)s+\1\b', text, flags=re.IGNORECASE))
print(re.findall(r'\b(\w+)\s+\1\b', text, flags=re.IGNORECASE))