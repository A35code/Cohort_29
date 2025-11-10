""" def ask_for_int(min_val = 1, max_val = 10, retries = 3):
    number = int(input("Guess a random number: "))
    try:
        number == range[min_val, max_val]

    except ValueError:
        print("Please give a number")

    except TypeError:
        print("Number not in range of values")

ask_for_int() """

#correction
class TooManyAttemptsError(Exception):
    """Raised when the user fails to many times."""
    pass

def ask_for_int(prompt, min_val, max_value, retries):
    """
    Ask the user for a number within a range
    -prompt: message to show the user
    -min_value: lowest allowed number
    -max_value: highest allowed number
    -retries: how many times a user can retry
    """

    attempts = 0 #counts how many retries the user has used

    #keps looping until retries run out

    while attempts < retries:
        try:
            #ask for input
            user_input = input(prompt)

            #convert input to integer
            num = int(user_input) #if this fails we get a ValueError

            #check if the input falls within the required range
            if num < min_val or num > max_value:
                print(f"Number is not within the range. Try again.")
                attempts += 1  
                if attempts == 3:
                    print("THAT WAS YOUR LAST ATTEMPT")
                else:
                    continue
                
                continue

            #if everything is okay, return the valid number
            return num
        except ValueError:
            print("That was not a avalid number , please try again.")
            attempts +=1

    raise TooManyAttemptsError("You failed too many times!")

try:
    range = ask_for_int("Enter your range: ", 5, 10, 3)
    print(f"You guessed right wit this number: {range}")

except TooManyAttemptsError as e:
    print(f"Game over: ", e)