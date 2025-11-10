try:
  with open("missing.txt", "r", encoding="utf-8") as f:
    print(f.read())
except FileNotFoundError:
  print("file was not found, please create the file or check path")