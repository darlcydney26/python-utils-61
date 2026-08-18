import re

def validate_input(user_input):
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    if len(user_input) == 0:
        raise ValueError("Input cannot be empty")
    if not re.match('^[a-zA-Z0-9_]+$', user_input):
        raise ValueError("Input must consist of alphanumeric characters and underscores only")
    return True

if __name__ == "__main__":
    while True:
        user_input = input("Enter a valid input: ")
        try:
            if validate_input(user_input):
                print("Valid input received!")
                break;
        except ValueError as e:
            print(e)
            print("Please try again.")