text = input("Enter a paragraph: ")

if text.strip() == "":
    print("No text entered.")
else:
    characters = len(text)
    words = len(text.split())
    spaces = text.count(" ")

    sentences = 0
    for char in text:
        if char in ".!?":
            sentences += 1

    print("\n--- Text Statistics ---")
    print("Characters:", characters)
    print("Words:", words)
    print("Sentences:", sentences)
    print("Spaces:", spaces)
