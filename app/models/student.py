students = {
    1: {
        "id": 1,
        "first_name": "Alex",
        "last_name": "Smith",
        "age": 20,
        "courses": ["python", "sql"]
    },
    2: {
        "id": 2,
        "first_name": "John",
        "last_name": "Brown",
        "age": 22,
        "courses": ["python"]
    }
}


def find_student(student_id: int):
    return students.get(student_id)


def list_students():
    return list(students.values())


def create_student(first_name: str, last_name: str, age: int, courses: list[str]):
    student_id = max(students, default=0) + 1

    student = {
        "id": student_id,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "courses": courses
    }

    students[student_id] = student
    return student


def update_student(student_id: int, first_name: str, last_name: str, age: int, courses: list[str]):
    student = students[student_id]

    student["first_name"] = first_name
    student["last_name"] = last_name
    student["age"] = age
    student["courses"] = courses

    return student


def delete_student(student_id: int):
    del students[student_id]