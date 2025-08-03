import json
import matplotlib.pyplot as plt

STUDENTS_FILE = "students.json"

def load_students():
    try:
        with open(STUDENTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_students(students):
    with open(STUDENTS_FILE, "w") as f:
        json.dump(students, f, indent=4)

def input_student():
    name = input("Ονοματεπώνυμο: ")
    am = input("ΑΜ: ")
    age = input("Ηλικία: ")
    courses = {}
    num = int(input("Αριθμός μαθημάτων: "))
    for _ in range(num):
        cname = input("Μάθημα: ")
        grade = float(input("Βαθμός: "))
        courses[cname] = grade
    return {"name": name, "am": am, "age": age, "courses": courses}

def calculate_avg(student):
    grades = list(student["courses"].values())
    return sum(grades) / len(grades) if grades else 0

def show_students(students, sort=False):
    if sort:
        students = sorted(students, key=calculate_avg, reverse=True)
    for s in students:
        avg = calculate_avg(s)
        print(f"\n{'-'*40}")
        print(f"{s['name']} (ΑΜ: {s['am']}, Ηλικία: {s['age']})")
        for course, grade in s['courses'].items():
            status = "Επιτυχία" if grade >= 5 else "Αποτυχία"
            print(f"  - {course}: {grade} ({status})")
        print(f"Μ.Ο.: {avg:.2f}")

def edit_grade(students):
    am = input("Δώσε ΑΜ φοιτητή: ")
    found = next((s for s in students if s["am"] == am), None)
    if not found:
        print("❌ Δεν βρέθηκε φοιτητής.")
        return
    course = input("Όνομα μαθήματος για διόρθωση: ")
    if course in found["courses"]:
        new_grade = float(input("Νέος βαθμός: "))
        found["courses"][course] = new_grade
        print("✅ Ενημερώθηκε.")
    else:
        print("❌ Δεν υπάρχει αυτό το μάθημα.")

def delete_grade(students):
    am = input("ΑΜ φοιτητή: ")
    found = next((s for s in students if s["am"] == am), None)
    if not found:
        print("❌ Δεν βρέθηκε φοιτητής.")
        return
    course = input("Μάθημα για διαγραφή: ")
    if course in found["courses"]:
        del found["courses"][course]
        print("✅ Διαγράφηκε.")
    else:
        print("❌ Δεν υπάρχει αυτό το μάθημα.")

def show_success_rates(students):
    course_stats = {}
    for s in students:
        for course, grade in s["courses"].items():
            if course not in course_stats:
                course_stats[course] = {"success": 0, "total": 0}
            course_stats[course]["total"] += 1
            if grade >= 5:
                course_stats[course]["success"] += 1
    print("\n📊 Ποσοστά επιτυχίας:")
    for course, data in course_stats.items():
        percent = (data["success"] / data["total"]) * 100
        print(f"  - {course}: {percent:.2f}%")

def plot_statistics(students):
    names = [s["name"] for s in students]
    avgs = [calculate_avg(s) for s in students]
    plt.figure(figsize=(10,5))
    plt.bar(names, avgs, color='skyblue')
    plt.title("Μέσος Όρος Φοιτητών")
    plt.xticks(rotation=45)
    plt.ylabel("Βαθμός")
    plt.tight_layout()
    plt.show()

def menu():
    students = load_students()
    while True:
        print("\n🧠 MENU")
        print("1. Προσθήκη φοιτητή")
        print("2. Εμφάνιση φοιτητών")
        print("3. Ταξινόμηση κατά Μ.Ο.")
        print("4. Διόρθωση βαθμού")
        print("5. Διαγραφή βαθμού")
        print("6. Ποσοστά επιτυχίας ανά μάθημα")
        print("7. Οπτική αναπαράσταση (γράφημα)")
        print("8. Αποθήκευση σε αρχείο")
        print("9. Έξοδος")

        ch = input("Επιλογή: ")
        if ch == "1":
            students.append(input_student())
        elif ch == "2":
            show_students(students)
        elif ch == "3":
            show_students(students, sort=True)
        elif ch == "4":
            edit_grade(students)
        elif ch == "5":
            delete_grade(students)
        elif ch == "6":
            show_success_rates(students)
        elif ch == "7":
            plot_statistics(students)
        elif ch == "8":
            save_students(students)
            print("✅ Αποθήκευση επιτυχής.")
        elif ch == "9":
            break
        else:
            print("❌ Μη έγκυρη επιλογή.")

if __name__ == "__main__":
    menu()
