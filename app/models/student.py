from pathlib import Path

from sqlalchemy import JSON, Column, Integer, MetaData, String, Table, create_engine, inspect, select


database_path = Path(__file__).resolve().parents[2] / "students.db"
engine = create_engine(f"sqlite:///{database_path}")

metadata = MetaData()

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("age", Integer, nullable=False),
    Column("courses", JSON, nullable=False),
)


def initialize_database():
    with engine.begin() as connection:
        if inspect(connection).has_table("students"):
            return

        metadata.create_all(connection)

        sample_students = [
            {
                "id": 1,
                "first_name": "Alex",
                "last_name": "Smith",
                "age": 20,
                "courses": ["python", "sql"]
            },
            {
                "id": 2,
                "first_name": "John",
                "last_name": "Brown",
                "age": 22,
                "courses": ["python"]
            }
        ]

        connection.execute(students.insert(), sample_students)


def find_student(student_id: int):
    query = select(students).where(students.c.id == student_id)

    with engine.connect() as connection:
        row = connection.execute(query).mappings().first()

        if row is None:
            return None

        return dict(row)


def list_students():
    query = select(students).order_by(students.c.id)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings()
        return [dict(row) for row in rows]


def create_student(first_name: str, last_name: str, age: int, courses: list[str]):
    query = students.insert().values(
        first_name=first_name,
        last_name=last_name,
        age=age,
        courses=courses
    )

    with engine.begin() as connection:
        result = connection.execute(query)
        student_id = result.inserted_primary_key[0]

        return {
            "id": student_id,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "courses": courses
        }


def update_student(
    student_id: int,
    first_name: str,
    last_name: str,
    age: int,
    courses: list[str]
):
    query = (
        students.update()
        .where(students.c.id == student_id)
        .values(
            first_name=first_name,
            last_name=last_name,
            age=age,
            courses=courses
        )
    )

    with engine.begin() as connection:
        connection.execute(query)

        query = select(students).where(students.c.id == student_id)
        row = connection.execute(query).mappings().one()

        return dict(row)


def delete_student(student_id: int):
    query = students.delete().where(students.c.id == student_id)

    with engine.begin() as connection:
        connection.execute(query)