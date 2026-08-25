def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b
def modulus(a, b):
    if b == 0:
        return "Cannot find modulus with zero"
    return a % b
print("Simple Calculator")
first_number = float(input("Enter first number: "))
second_number = float(input("Enter second number: "))
print("\nResults")
print("Addition:", add(first_number, second_number))
print("Subtraction:", subtract(first_number, second_number))
print("Multiplication:", multiply(first_number, second_number))
print("Division:", divide(first_number, second_number))
print("Modulus:", modulus(first_number, second_number))