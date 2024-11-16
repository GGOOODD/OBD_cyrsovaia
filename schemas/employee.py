from pydantic import BaseModel
from datetime import datetime


class EmployeeInfo(BaseModel):
    job_title_id: int
    name: str
    surname: str
    patronymic: str
    experience: str


class GetEmployee(BaseModel):
    id: int
    job_title_id: int
    name: str
    surname: str
    patronymic: str
    experience: str


class CrewInfo(BaseModel):
    flight_id: int
    employee_id: int


class GetCrew(BaseModel):
    id: int
    flight_id: int
    employee_id: int
