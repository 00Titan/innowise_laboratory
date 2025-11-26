def valid_name(name: str) -> bool:
    # Check if value is a valid student name (no digits, at least one letter)
    allowed_extra = {" ", "-", "'"}
    if not isinstance(name, str):
        return False
    name = name.strip()
    if not name:
        return False
    if any(ch.isdigit() for ch in name):
        return False
    if not any(ch.isalpha() for ch in name):
        return False
    for ch in name:
        if not (ch.isalpha() or ch in allowed_extra):
            return False
    return True


def add_student(students: list, names: set):
    # Prompt for a name, validate and add a new student record
    name = input("Enter student name: ").strip()
    if not valid_name(name):
        print("Invalid input. Please enter a correct name.")
        return None

    if name.lower() in names:
        print("Student with this name already exists.")
        return None
    else:
        names.add(name.lower())
        students.append({"name": name, "grades": []})
        return None


def add_grade(students: list, names: set):
    # Prompt for student name and then accept integer grades until 'done'
    name = input("Enter student name: ").strip()
    if name.lower() not in names:
        print("Student with this name doesn't exist.")
        return None
    for student in students:
        if student["name"].lower() == name.lower() :
            while True:
                grade = input("Enter a grade (or 'done' to finish): ").strip()
                if grade.lower() == 'done':
                    break
                try:
                    grade = int(grade)
                    if not 0 <= grade <= 100:
                        raise ValueError
                except ValueError:
                    print("Invalid input. Please enter a number (0- 100).")
                    print()
                    continue
                student["grades"].append(grade)
            break
    else:
        print("Student with this name not found.")
        return None


def are_grades_entered(students:list) -> bool:
    # Return True if at least one student has grades
    return any(isinstance(s, dict) and s.get("grades") for s in students)


def show_report(students: list):
    # Print averages for each student and overall statistics
    if not students:
        print("No student added")
        return None

    if not are_grades_entered(students):
        # If nobody has grades, report N/A for each student
        for s in students:
            name = s.get("name", "Unknown") if isinstance(s, dict) else "Unknown"
            print(f"{name}'s average grade is N/A.")
        print("No grades added.")
        return None

    averages = []
    for s in students:
        if not isinstance(s, dict) or "name" not in s:
            print("Invalid student entry found, skipping.")
            continue
        grades = s.get("grades", [])
        if not grades:
            print(f"{s['name']}'s average grade is N/A.")
        else:
            avg = sum(grades) / len(grades)
            averages.append(avg)
            print(f"{s['name']}'s average grade is {avg:.1f}.")

    if averages:
        # Print summary statistics: max, min, overall average
        print("--------------------------")
        print(f"Max Average: {max(averages):.1f}")
        print(f"Min Average: {min(averages):.1f}")
        overall = sum(averages) / len(averages)
        print(f"Overall Average: {overall:.1f}")
    return None


def find_top_performer(students:list):
    # Find and print the student with the highest average grade
    if not students:
        print("No student added.")
        return None

    scored = [s for s in students if isinstance(s, dict) and s.get("grades")]
    if not scored:
        print("No grades added.")
        return None

    top = max(scored, key=lambda s: sum(s["grades"]) / len(s["grades"]))
    top_avg = sum(top["grades"]) / len(top["grades"])
    print(f"The student with the highest average is {top['name']} with a grade of {top_avg:.1f}.")
    return None


def main():
    # Main interactive loop that shows menu and handles user choices
    names = set()
    students = []
    while True:
        print("--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Generate a full report")
        print("4. Find top student")
        print("5. Exit program")
        option = input("Enter your choice: ").strip()

        try:
            choice = int(option)
            if choice not in [1, 2, 3, 4, 5]:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 5.")
            print()
            continue

        if choice == 1:
            add_student(students=students, names=names)
        elif choice == 2:
            add_grade(students=students, names=names)
        elif choice == 3:
            show_report(students=students)
        elif choice == 4:
            find_top_performer(students=students)
        elif choice == 5:
            print("Exiting program.")
            break
        print()


if __name__ == "__main__":
    main()