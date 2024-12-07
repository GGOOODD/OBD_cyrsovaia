from pydantic import BaseModel
from datetime import datetime


class FlightHistoryInfo(BaseModel):
    scheduled_flight_id: int


class GetFlightHistory(BaseModel):
    airline: str
    destination: str
    airport: str
    payment_datetime: datetime
    seat: str


class UpdPassword(BaseModel):
    password: str


class UpdFIO(BaseModel):
    name: str
    surname: str
    patronymic: str
