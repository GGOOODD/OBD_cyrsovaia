from pydantic import BaseModel, constr


class ShopData(BaseModel):
    name: str
    location: str


class CountryData(BaseModel):
    name: constr(max_length=100)
    geocode: constr(max_length=3)


class SettlementData(BaseModel):
    name: constr(max_length=100)
    countryName: constr(max_length=100)
    settlementType: constr(max_length=50)


class AirportData(BaseModel):
    name: constr(max_length=100)
    settlementName: constr(max_length=100)
    address: constr(max_length=256)


class FlightData(BaseModel):
    airlineName: constr(max_length=100)
    airportName: constr(max_length=100)


class AirlineData(BaseModel):
    name: constr(max_length=100)


class SchFlightModelData(BaseModel):
    name: constr(max_length=100)


class AirplaneModelData(BaseModel):
    name: constr(max_length=100)
    capacity: int


class AirplaneData(BaseModel):
    airplaneModelName: constr(max_length=100)
    registrationNumber: constr(max_length=100)


class MaintenanceModelData(BaseModel):
    name: constr(max_length=100)
    description: constr(max_length=1024)


class JobTitleData(BaseModel):
    name: constr(max_length=100)


class EmployeeData(BaseModel):
    jobTitleName: constr(max_length=100)
    surname: constr(max_length=100)
    name: constr(max_length=100)
    patronymic: constr(max_length=100)
    experience: constr(max_length=50)


class PretripMaintenanceData(BaseModel):
    maintenanceModelName: constr(max_length=100)
    surname: constr(max_length=100)
    name: constr(max_length=100)
    patronymic: constr(max_length=100)
    experience: constr(max_length=50)
    registrationNubmer: constr(max_length=100)
    datetime: constr(max_length=100)
    result: constr(max_length=100)


class ScheduledFlightData(BaseModel):
    airlineName: constr(max_length=100)
    airportName: constr(max_length=100)
    datetimeDeparture: constr(max_length=100)
    datetimeArrival: constr(max_length=100)
    registrationNumber: constr(max_length=100)
    scheduledFlightModelName: constr(max_length=100)
    crew: list[int]
