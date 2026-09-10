print("Student Grade Calculator")
print("------------------------")
subjects = int(input("Enter number of subjects: "))
total_marks = 0
for i in range(subjects):
    mark = float(input(f"Enter marks for subject {i + 1}: "))
    while mark < 0 or mark > 100:
        print("Please enter marks between 0 and 100.")
        mark = float(input(f"Enter marks for subject {i + 1}: "))
    total_marks += mark
percentage = total_marks / subjects
if percentage >= 90:
    grade = "A+"
elif percentage >= 80:
    grade = "A"
elif percentage >= 70:
    grade = "B"
elif percentage >= 60:
    grade = "C"
elif percentage >= 50:
    grade = "D"
else:
    grade = "F"
print("\nStudent Result")
print("-------------")
print(f"Total Marks: {total_marks}")
print(f"Percentage: {percentage:.2f}%")
print(f"Grade: {grade}")