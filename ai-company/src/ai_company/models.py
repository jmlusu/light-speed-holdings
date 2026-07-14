from pydantic import BaseModel

class Executive(BaseModel):

    id: str

    title: str

    department: str

    role: str

    reports_to: str
class BoardAdvisor(BaseModel):

    id: str

    title: str

    inspiration: list[str]
class Specialist(BaseModel):

    title: str

    reports_to: str