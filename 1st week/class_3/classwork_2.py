class TooManyAttemptsError(Exception):
    """Raised when the user fails too many times to log in."""

    pass


def ask_for_int(message, min_val, max_val, retries):
    """Ask the user for a number within a range.
    - message: this is the message to show the user
    - min_val: lowest acceptable value
    - max_val: highest acceptable value
    - retries: number of allowed retries
    """

    lives_used = 0
    # keep asking until the user runs out of lives_used
    while lives_used < retries:
        try:
            # step 1 - ask user for input
            user_input = int(input(message))

            # step 2 - check if it's within the range
            if user_input < min_val or user_input > max_val:
                lives_used += 1
                print(f"Wrong Guess Try Again. You have {retries - lives_used} lives_used left.")
                continue

            # step 3 - if we get here, the input is valid
            else:
                return user_input

        except ValueError:
            # Happens if the user types something that's not a number
            print("Invalid input. Please enter a number.")
            lives_used += 1
            continue

    # if we get here, the user has run out of lives_used
    raise TooManyAttemptsError("Too many invalid attempts.")


try:
    number = ask_for_int("Enter a number: ", 1, 10, retries=3)
    print(f"Congrats you were right, you entered {number}")

except TooManyAttemptsError as e:
    print(f"Sorry, Game over: {e}")
