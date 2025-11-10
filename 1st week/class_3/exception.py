def divide_inputs():
    try:
        a = int(input("Enter numerator"))
        b = int(input("Enter denominator"))
        result = a / b
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    else:
        print("Result:", result)
    finally:
        print("Done - thanks for trying!.")

divide_inputs()