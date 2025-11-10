#f = open("log.txt", "a", encoding="utf-8")
#f.write("action taken: jump\n")
#f.write("action taken: run\n")
#f.write("action taken: sleep\n")
#f.write("action taken: cry\n")
#f.close()

with  open("log.txt", "r", encoding="utf-8") as f:
    print(f.read())