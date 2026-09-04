text = input("Enter a word or sentence: ")
normalized_text = text.lower().replace(" ", "")
if normalized_text == normalized_text[::-1]:
    print("Result: It is a palindrome.")
else:
    print("Result: It is not a palindrome.")
