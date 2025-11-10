""" def divide_inputs():
    try:
        a = int(input("Numerator: "))
        b = int(input("Denominator: "))
        result = a / b
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")

    else:
        print(f"The final result is {result}")
    finally:
        print("Done - thank you for using divider")

divide_inputs() """

def second_item(x):
    try:
        return x[1]
    
    except (ValueError, TypeError) as e:
        return f"Error: {e}"
    
    #except TypeError:
    #    print("Please return the second input")
#    except IndexError:
#        print("Please return the sequence of the list")
    finally:
        print("Thank you for using our app and have a nice day 👋")

print(second_item([1, 2]))