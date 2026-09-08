from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class StudentBody(BaseModel):
    first_name: str
    last_name: str
    age: int
    courses: list[str]


app = FastAPI(title="Students Service")


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
    student = students.get(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.get("/students")
def list_students():
    return list(students.values())


@app.get("/students/{student_id}")
def get_student(student_id: int):
    return find_student(student_id)


@app.post("/students")
def create_student(body: StudentBody):
    student_id = max(students.keys(), default=0) + 1

    student = {
        "id": student_id,
        "first_name": body.first_name,
        "last_name": body.last_name,
        "age": body.age,
        "courses": body.courses
    }

    students[student_id] = student

    return student


@app.patch("/students/{student_id}")
def update_student(student_id: int, body: StudentBody):
    student = find_student(student_id)

    student["first_name"] = body.first_name
    student["last_name"] = body.last_name
    student["age"] = body.age
    student["courses"] = body.courses

    return student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    find_student(student_id)
    del students[student_id]