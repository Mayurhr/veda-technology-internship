def calculate_subtotal(products):
    subtotal = 0

    for product in products:
        subtotal += product["price"] * product["quantity"]

    return subtotal

def calculate_discount(subtotal):
    if subtotal >= 5000:
        return subtotal * 0.10
    elif subtotal >= 2000:
        return subtotal * 0.05
    else:
        return 0

def calculate_tax(amount):
    return amount * 0.05

products = []

print("===== SHOPPING BILL GENERATOR =====")

n = int(input("Enter number of products: "))

for i in range(n):
    print("\nProduct", i + 1)

    name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    product = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    products.append(product)

subtotal = calculate_subtotal(products)
discount = calculate_discount(subtotal)
amount_after_discount = subtotal - discount
tax = calculate_tax(amount_after_discount)
final_amount = amount_after_discount + tax

print("\n========== SHOPPING BILL ==========")
print(f"{'Product':<15}{'Qty':<8}{'Price':<10}{'Total':<10}")

for product in products:
    total = product["price"] * product["quantity"]
    print(
        f"{product['name']:<15}"
        f"{product['quantity']:<8}"
        f"{product['price']:<10.2f}"
        f"{total:<10.2f}"

print("-----------------------------------")
print(f"Subtotal:              ₹{subtotal:.2f}")
print(f"Discount:              ₹{discount:.2f}")
print(f"Tax:                   ₹{tax:.2f}")
print(f"Final Amount:          ₹{final_amount:.2f}")
print("===================================")
