import re

# Validate phone number input
def input_phone(input_fn=input, prompt="Enter your Phone Number (0XXXXXXXXXX): "):
    while True:
        user_input = input_fn(prompt).strip()
        # Convert +234XXXXXXXXXX to 0XXXXXXXXXX
        if user_input.startswith('+234'):
            user_input = '0' + user_input[4:]
        # Must start with 0 and be 11 digits
        if re.match(r'^0\d{10}$', user_input):
            return user_input
        print("Invalid phone number. Use 0XXXXXXXXXX and it must be 11 digits.")

# Validate PIN input (4 or 6 digits)
def input_pin(input_fn=input, prompt="Enter your 4 or 6-digit PIN: "):
    while True:
        entered_pin = input_fn(prompt).strip()
        if entered_pin.isdigit() and len(entered_pin) in (4, 6):
            confirmed_pin = input_fn("Confirm your PIN: ").strip()
            if entered_pin == confirmed_pin:
                return entered_pin
            else:
                print("PINs do not match. Please try again.")
        else:
            print("PIN must be numeric and 4 or 6 digits.")

# Validate non-empty text input (e.g., Name, Location)
def input_non_empty_text(input_fn=input, prompt="Enter your Name: "):
    while True:
        user_text = input_fn(prompt).strip()
        # Must not be empty and must contain at least one letter
        if user_text and any(char.isalpha() for char in user_text):
            return user_text
        print("Input cannot be empty or just numbers. Please enter valid text.")

# Validate positive float input (e.g., Farm Size, Price)
def input_positive_float(input_fn=input, prompt="Enter a number: "):
    while True:
        user_input = input_fn(prompt).strip()
        try:
            numeric_value = float(user_input)
            if numeric_value > 0:
                return numeric_value
            else:
                print("Number must be greater than 0. Please try again.")
        except ValueError:
            print("Invalid number. Please enter a numeric value.")

# Validate crop/product list input (comma separated)
def input_crops_list(input_fn=input, prompt="Enter your Crops (comma separated): "):
    while True:
        raw_input_text = input_fn(prompt).strip()
        crops_list = [crop.strip() for crop in raw_input_text.split(",") if crop.strip()]
        # Must contain at least one valid crop name
        if crops_list and all(any(char.isalpha() for char in crop) for crop in crops_list):
            return crops_list
        print("Please enter at least one valid crop name, separated by commas if multiple.")
