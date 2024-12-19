from pydantic import BaseModel

class Student(BaseModel):
    name: str
    grade: float
    photo_url: str