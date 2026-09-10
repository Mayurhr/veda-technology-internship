# Temperature Converter

## Description

This project is a Python program that converts temperatures between Celsius, Fahrenheit, and Kelvin.

## Objective

Practice functions, arithmetic operations, input validation, and formatted output.

## Features

- Convert between Celsius, Fahrenheit, and Kelvin
- Use separate functions for each conversion
- Validate temperature and unit input
- Reject temperatures below absolute zero
- Format results to two decimal places

## How the Program Works

1. The program asks for a temperature value.
2. It asks for the source unit and target unit.
3. It validates the units and checks that the temperature is physically meaningful.
4. It applies the correct conversion formula.
5. It displays the converted temperature with two decimal places.

## Conversion Formulas

- Celsius to Fahrenheit: `F = (C * 9 / 5) + 32`
- Fahrenheit to Celsius: `C = (F - 32) * 5 / 9`
- Celsius to Kelvin: `K = C + 273.15`
- Kelvin to Celsius: `C = K - 273.15`
- Fahrenheit to Kelvin: `K = ((F - 32) * 5 / 9) + 273.15`
- Kelvin to Fahrenheit: `F = ((K - 273.15) * 9 / 5) + 32`

## How to Run

```text
python temperature_converter.py
```

## Sample Output

See `sample_output.txt` for examples of Celsius to Fahrenheit, Fahrenheit to Celsius, Celsius to Kelvin, Kelvin to Celsius, and invalid input.

## Concepts Learned

- Functions
- Parameters and return values
- Arithmetic operations
- Conditional statements
- Input validation
- String methods
- Formatted output
