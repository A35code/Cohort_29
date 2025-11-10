with open("image.png", "rb") as fsr, open("copy.png", "ab") as far:
    first_image = fsr.read()
    far.write(first_image)
    #print(first_image)