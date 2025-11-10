f = open("trial.txt", "r", encoding="utf-8")
#print(f.read()) reads whole file
#print(f.readline())
#print(f.readline()) reads line by line
import sys

# Ensure stdout can handle UTF-8 on Windows (Python 3.7+)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # Fallback for older Pythons: wrap stdout with a TextIOWrapper
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

f = open("trial.txt", "r", encoding="utf-8")
# print(f.read()) reads whole file
# print(f.readline())
# print(f.readline()) reads line by line
content = f.readlines()
for name in content:
    print(name.rstrip('\n'))

# "r" = read
# "a" = append
# "w" = write
# "x" = create
# RAWX