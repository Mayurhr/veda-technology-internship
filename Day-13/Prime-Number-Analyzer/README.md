# Prime Number Analyzer

## Description

This project is a Python program that checks whether a number is prime and generates all prime numbers within a specified range.

## Features

- Check whether a number is prime
- Generate prime numbers in a range
- Handle 0 and 1 correctly
- Reusable `is_prime()` function
- Menu-driven interface

## Technologies Used

- Python

## Concepts Used

- Functions
- Loops
- Conditional statements
- Modulus operator
- `range()`
- Basic algorithm optimization

## Algorithm

A prime number is a number greater than 1 that has exactly two factors: 1 and itself.

For a number `n`:

1. If `n` is less than 2, it is not prime.
2. Check divisibility starting from 2.
3. Only check up to the square root of `n`.
4. If any number divides `n` exactly, it is not prime.
5. Otherwise, it is prime.

Checking only up to the square root avoids unnecessary divisibility checks. If a number has a factor larger than its square root, it must also have a smaller factor that would already have been found.

The prime-checking function takes O(sqrt(n)) time in the worst case, which is the algorithm's time complexity.

## How to Run

```text
python prime_number_analyzer.py
```

## Sample Output

```text
--- Prime Number Analyzer ---
1. Check Prime Number
2. Generate Prime Numbers
3. Exit
Enter your choice: 1
Enter a number: 17
17 is a prime number.
```

## Internship

Veda Technology Python Programming Internship

Day 13 - Prime Number Analyzer
