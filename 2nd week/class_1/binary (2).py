# with open("image.png", "rb") as fsrc, open("copy.png", "wb") as fdst:
#     fdst.write(fsrc.read())


with open("image.png", "rb") as fsrc, open("copy.png", "wb") as fdst:
  first_image = fsrc.read()
  fdst.write(first_image)