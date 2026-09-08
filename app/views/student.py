from pydantic import BaseModel


class StudentView(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    courses: list[str]