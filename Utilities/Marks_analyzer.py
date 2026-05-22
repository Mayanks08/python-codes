

def collect_student_data():
    students={}

    while True:
        name = input("Enter name:").strip()

        if name.lower() == "done":
            break
        if name in students:
            print("name already exist")
            continue

        try:
            marks=float(input("Enter marks:").strip())
            students[name]=marks
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return students

def analyze_data(students):
    if not students:
        print("No data found")
        return
    
    marks = list(students.values())
    max_score = max(marks)
    min_score = min(marks)
    avg_score = sum(marks) / len(marks)
    passing_students = [name for name, mark in students.items() if mark >= 50]
    
    topper = [name for name, mark in students.items() if mark == max_score]
    bottomer = [name for name, mark in students.items() if mark == min_score]

    print("\n Students marks Report")
    print("-"*30)
    print(f"Total students: {len(students)}")
    print(f"Average marks: {avg_score:.2f}")
    print(f"Highest score: {max_score} by {', '.join(topper)}")
    print(f"Lowest score: {min_score} by {', '.join(bottomer)}")

    print("-" * 30)
    print("Detailed Marks")
    for name, score in students.items():
        print(f"-{name} : {score}")
        if score >=80:
            grade="A"
        elif score>=60:
            grade="B"
        elif score>=50:
            grade="C"
        else:
            grade="F"
        print(f"-{name} : {score} ({grade})")
        if score>=50:
            print("Pass")
        else:
            print("Fail")


students = collect_student_data()
analyze_data(students)


