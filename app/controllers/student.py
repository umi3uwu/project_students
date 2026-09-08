from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models import student as models
from app.views.student import StudentView


router = APIRouter(prefix="/students")


class StudentBody(BaseModel):
    first_name: str
    last_name: str
    age: int
    courses: list[str]


def find_student_or_404(student_id: int):
    student = models.find_student(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.get("", response_model=list[StudentView])
def list_students():
    return models.list_students()


@router.get("/{student_id}", response_model=StudentView)
def get_student(student_id: int):
    return find_student_or_404(student_id)


@router.post("", response_model=StudentView)
def create_student(body: StudentBody):
    return models.create_student(
        body.first_name,
        body.last_name,
        body.age,
        body.courses
    )


@router.patch("/{student_id}", response_model=StudentView)
def update_student(student_id: int, body: StudentBody):
    find_student_or_404(student_id)

    return models.update_student(
        student_id,
        body.first_name,
        body.last_name,
        body.age,
        body.courses
    )


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int):
    find_student_or_404(student_id)
    models.delete_student(student_id)