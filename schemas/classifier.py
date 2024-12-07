from pydantic import BaseModel


class ShopData(BaseModel):
    name: str
    location: str


class CountryData(BaseModel):
    name: str
    geocode: str


class SettlementData(BaseModel):
    name: str
    countryName: str
    settlementType: str


class AirportData(BaseModel):
    name: str
    settlementName: str
    address: str


class FlightData(BaseModel):
    airlineName: str
    airportName: str


class AirlineData(BaseModel):
    name: str


class SchFlightModelData(BaseModel):
    name: str


class AirplaneModelData(BaseModel):
    name: str
    capacity: int


class AirplaneData(BaseModel):
    airplaneModelName: str
    registrationNumber: str


class MaintenanceModelData(BaseModel):
    name: str
    description: str


class JobTitleData(BaseModel):
    name: str


class EmployeeData(BaseModel):
    jobTitleName: str
    surname: str
    name: str
    patronymic: str
    experience: str


class PretripMaintenanceData(BaseModel):
    maintenanceModelName: str
    surname: str
    name: str
    patronymic: str
    experience: str
    registrationNubmer: str
    datetime: str
    result: str


class ScheduledFlightData(BaseModel):
    airlineName: str
    airportName: str
    datetimeDeparture: str
    datetimeArrival: str
    registrationNumber: str
    scheduledFlightModelName: str
    crew: list[int]
