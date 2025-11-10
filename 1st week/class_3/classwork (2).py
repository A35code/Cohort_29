def second_item(x):
  try:
    return x[1]
  except IndexError:
    return "List is too short."
  except TypeError:
    return "Input must be a list."
  else:
    return "Second item is:", x[1]

print(second_item(1))