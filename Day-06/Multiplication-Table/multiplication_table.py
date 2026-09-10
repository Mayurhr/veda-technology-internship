print("Multiplication Table")
print("--------------------")
number = int(input("Enter a number: "))
limit = int(input("Enter the limit: "))
print(f"\nMultiplication table of {number}")
print("----------------------------")
for i in range(1, limit + 1):
    result = number * i
    print(f"{number} x {i} = {result}")
