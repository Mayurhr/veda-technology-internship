students = ["Mayur", "Rahul", "Anil", "Sneha"]
marks = [85, 72, 91, 78]

print("Student Records")
print("----------------")

for i in range(len(students)):
    print(students[i], "-", marks[i])

print("\nHighest Score:")
highest = max(marks)
index = marks.index(highest)
print(students[index], "-", highest)

print("\nLowest Score:")
lowest = min(marks)
index = marks.index(lowest)
print(students[index], "-", lowest)

print("\nSorted Marks:")
sorted_marks = sorted(marks)
print(sorted_marks)

search_name = input("\nEnter student name to search: ")

if search_name in students:
    index = students.index(search_name)
    print(search_name, "has scored", marks[index])
else:
    print("Student not found.")
