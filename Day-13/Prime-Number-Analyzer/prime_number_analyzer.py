def is_prime(number):
    """Return True when number is a prime number."""
    if number < 2:
        return False

    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1

    return True


def check_prime():
    number = int(input("Enter a number: "))

    if is_prime(number):
        print(f"{number} is a prime number.")
    else:
        print(f"{number} is not a prime number.")


def generate_primes():
    start = int(input("Enter the starting number: "))
    end = int(input("Enter the ending number: "))

    primes = []
    for number in range(start, end + 1):
        if is_prime(number):
            primes.append(number)

    if primes:
        print("Prime numbers:", ", ".join(map(str, primes)))
    else:
        print("No prime numbers found in this range.")


def main():
    while True:
        print("\n--- Prime Number Analyzer ---")
        print("1. Check Prime Number")
        print("2. Generate Prime Numbers")
        print("3. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                check_prime()
            elif choice == "2":
                generate_primes()
            elif choice == "3":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Please enter valid whole numbers.")


if __name__ == "__main__":
    main()
