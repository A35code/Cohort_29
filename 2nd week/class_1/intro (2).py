# f = open("trial.txt", "r", encoding="utf-8")
# print(f.read())
# print(f.readline())
# content = f.readlines()
# for name in content:
#   print(name)
# f.close()


# f = open("log.txt", "a", encoding="utf-8")
# f.write("Action taken: sleep\n")
# f.write("Action taken: cry\n")
# f.write("Action taken: laugh\n")
# f.close()

with open("test.txt", "r", encoding="utf-8") as f:
  print(f.read())