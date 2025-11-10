from datetime import datetime, timedelta

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor '{name}' already signed in last! No back-to-back visits allowed."
        super().__init__(self.message)

# Define a custom exception for time restriction
class TimeRestrictionError(Exception):
    def __init__(self, minutes_left):
        self.message = f"Please wait {minutes_left:.1f} more minutes before adding a new visitor."
        super().__init__(self.message)

def main():
    filename = "visitors.txt"

    # Ensure the file exists
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print("File not found, creating a new file.")
        with open(filename, "w", encoding="utf-8") as f:
            pass

    visitor = input("Enter visitor's name: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        last_visitor = None
        last_time = None

        if lines:
            last_entry = lines[-1].strip()
            parts = last_entry.split(" | ")
            if len(parts) == 2:
                last_visitor, last_time_str = parts
                last_time = datetime.fromisoformat(last_time_str.strip())

        # Check 1: Same visitor twice in a row
        if visitor == last_visitor:
            raise DuplicateVisitorError(visitor)

        # Check 2: Less than 5 minutes since last visitor
        if last_time:
            time_diff = datetime.now() - last_time
            if time_diff < timedelta(minutes=5):
                minutes_left = 5 - (time_diff.total_seconds() / 60)
                raise TimeRestrictionError(minutes_left)

        # Append the new visitor
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now().isoformat()}\n")

        print("Visitor added successfully!")

    except (DuplicateVisitorError, TimeRestrictionError) as e:
        print("Error:", e)

# Run the program
main()
