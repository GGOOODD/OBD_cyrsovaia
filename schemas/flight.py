from pydantic import BaseModel
from datetime import datetime


class FlightInfo(BaseModel):
    airline_id: int
    airport_id: int


class GetFlight(BaseModel):
    id: int
    airline_id: int
    airport_id: int


class ScheduledFlightInfo(BaseModel):
    flight_id: int
    scheduled_flight_model_id: int
    airplane_id: int
    departure_datetime: datetime
    arrival_datetime: datetime


class GetScheduledFlight(BaseModel):
    id: int
    flight_id: int
    scheduled_flight_model_id: int
    airplane_id: int
    departure_datetime: datetime
    arrival_datetime: datetime


class AirplaneInfo(BaseModel):
    airplane_model_id: int
    registration_number: int


class GetAirplane(BaseModel):
    id: int
    airplane_model_id: int
    registration_number: int


class PretripMaintenanceInfo(BaseModel):
    maintenance_model_id: int
    employee_id: int
    airplane_id: int
    datetime: datetime
    result: str


class GetPretripMaintenance(BaseModel):
    id: int
    maintenance_model_id: int
    employee_id: int
    airplane_id: int
    datetime: datetime
    result: str
