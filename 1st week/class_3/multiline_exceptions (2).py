try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print("Value/Type Problem:", e)
