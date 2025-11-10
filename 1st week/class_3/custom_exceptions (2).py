class TooManyAttemptsError(Exception):
    pass

class WrongPasswordOrUsernameError(Exception):
    pass

def login(user, password):
    if not user or not password:
        raise ValueError("Username and password are required.")
    # Simulate a login attempt
    if user != "admin" or password != "secret":
        raise WrongPasswordOrUsernameError("Invalid username or password.")

login("admin", "wrongpassword")
