students = []

with open("practice_2.1/resource/students.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        name_part, grades_part = line.split(":")
        grades = list(map(int, grades_part.split(",")))
        avg = sum(grades) / len(grades)

        students.append((name_part, grades, avg))

with open("practice_2.1/resource/result.txt", "w", encoding="utf-8") as f:
    for name, grades, avg in students:
        if avg > 4.0:
            f.write(f"{name}:{avg:.2f}\n")

best_student = max(students, key=lambda x: x[2])
worst_student = min(students, key=lambda x: x[2])

print("Студент с наивысшим средним баллом:")
print(f"{best_student[0]} — {best_student[2]:.2f}")

print("Студент с низким средним баллом:")
print(f"{worst_student[0]} — {worst_student[2]:.2f}")