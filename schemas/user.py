from pydantic import BaseModel
from datetime import datetime


class FlightHistoryInfo(BaseModel):
    scheduled_flight_id: int
    payment_datetime: datetime
    seat: str


class GetFlightHistory(BaseModel):
    id: int
    user_id: int
    scheduled_flight_id: int
    payment_datetime: datetime
    seat: str
