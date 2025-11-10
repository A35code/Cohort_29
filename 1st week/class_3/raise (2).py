def withdraw(balance, amount):
    if amount > balance:
      raise ValueError("Insufficient funds")
    return balance - amount


print(withdraw(50, 100))
