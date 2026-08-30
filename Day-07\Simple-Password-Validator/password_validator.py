import string
password = input("Enter your password: ")
has_upper = False
has_lower = False
has_digit = False
has_special = False
for char in password:
    if char.isupper():
        has_upper = True
    elif char.islower():
        has_lower = True
    elif char.isdigit():
        has_digit = True
    elif char in string.punctuation:
        has_special = True
if len(password) < 8:
    print("Password must contain at least 8 characters.")
elif not has_upper:
    print("Password must contain an uppercase letter.")
elif not has_lower:
    print("Password must contain a lowercase letter.")
elif not has_digit:
    print("Password must contain a number.")
elif not has_special:
    print("Password must contain a special character.")
else:
    print("Password is valid.")
