def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def kelvin_to_fahrenheit(kelvin):
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


def is_valid_temperature(value, unit):
    if unit == "C":
        return value >= -273.15
    if unit == "F":
        return value >= -459.67
    return value >= 0


def convert_temperature(value, source_unit, target_unit):
    if source_unit == target_unit:
        return value
    if source_unit == "C" and target_unit == "F":
        return celsius_to_fahrenheit(value)
    if source_unit == "F" and target_unit == "C":
        return fahrenheit_to_celsius(value)
    if source_unit == "C" and target_unit == "K":
        return celsius_to_kelvin(value)
    if source_unit == "K" and target_unit == "C":
        return kelvin_to_celsius(value)
    if source_unit == "F" and target_unit == "K":
        return fahrenheit_to_kelvin(value)
    return kelvin_to_fahrenheit(value)


def main():
    print("--- Temperature Converter ---")

    try:
        temperature = float(input("Enter the temperature value: "))
    except ValueError:
        print("Invalid temperature. Please enter a number.")
        return

    source_unit = input("Enter the source unit (C, F, or K): ").strip().upper()
    target_unit = input("Enter the target unit (C, F, or K): ").strip().upper()

    if source_unit not in ("C", "F", "K") or target_unit not in ("C", "F", "K"):
        print("Invalid unit choice. Please use C, F, or K.")
        return

    if not is_valid_temperature(temperature, source_unit):
        print("Invalid temperature. It cannot be below absolute zero.")
        return

    result = convert_temperature(temperature, source_unit, target_unit)
    print(f"Result: {result:.2f} {target_unit}")


if __name__ == "__main__":
    main()