from fastapi import APIRouter, status, Request
from schemas import *
from services import Classifier

router = APIRouter(tags=["Classifier"], prefix="/classifier")


# SHOP -----------------------------------------------------------------------------------------------------------
@router.get("/get_all_shop", status_code=status.HTTP_200_OK)
async def get_all_shop():
    return await Classifier.get_all_shop()


@router.post("/create_shop", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_shop(data: ShopData, request: Request):
    return await Classifier.create_shop(data, request)


@router.put("/update_shop/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_shop(field_id: int, data: ShopData, request: Request):
    return await Classifier.update_shop(field_id, data, request)


@router.delete("/delete_shop/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_shop(field_id: int, request: Request):
    return await Classifier.delete_shop(field_id, request)


# COUNTRY ---------------------------------------------------------------------------------------------------------
@router.get("/get_all_country", status_code=status.HTTP_200_OK)
async def get_all_country(request: Request):
    return await Classifier.get_all_country(request)


@router.post("/create_country", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_country(data: CountryData, request: Request):
    return await Classifier.create_country(data, request)


@router.put("/update_country/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_country(field_id: int, data: CountryData, request: Request):
    return await Classifier.update_country(field_id, data, request)


@router.delete("/delete_country/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_country(field_id: int, request: Request):
    return await Classifier.delete_country(field_id, request)


# SETTLEMENT ------------------------------------------------------------------------------------------------------
@router.get("/get_all_settlement", status_code=status.HTTP_200_OK)
async def get_all_settlement(request: Request):
    return await Classifier.get_all_settlement(request)


@router.post("/create_settlement", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_settlement(data: SettlementData, request: Request):
    return await Classifier.create_settlement(data, request)


@router.put("/update_settlement/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_settlement(field_id: int, data: SettlementData, request: Request):
    return await Classifier.update_settlement(field_id, data, request)


@router.delete("/delete_settlement/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_settlement(field_id: int, request: Request):
    return await Classifier.delete_settlement(field_id, request)


# AIRPORT ------------------------------------------------------------------------------------------------------
@router.get("/get_all_airport", status_code=status.HTTP_200_OK)
async def get_all_airport(request: Request):
    return await Classifier.get_all_airport(request)


@router.post("/create_airport", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airport(data: AirportData, request: Request):
    return await Classifier.create_airport(data, request)


@router.put("/update_airport/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airport(field_id: int, data: AirportData, request: Request):
    return await Classifier.update_airport(field_id, data, request)


@router.delete("/delete_airport/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airport(field_id: int, request: Request):
    return await Classifier.delete_airport(field_id, request)


# FLIGHT --------------------------------------------------------------------------------------------------------
@router.get("/get_all_flight", status_code=status.HTTP_200_OK)
async def get_all_flight(request: Request):
    return await Classifier.get_all_flight(request)


@router.post("/create_flight", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_flight(data: FlightData, request: Request):
    return await Classifier.create_flight(data, request)


@router.put("/update_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_flight(field_id: int, data: FlightData, request: Request):
    return await Classifier.update_flight(field_id, data, request)


@router.delete("/delete_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_flight(field_id: int, request: Request):
    return await Classifier.delete_flight(field_id, request)


# AIRLINE --------------------------------------------------------------------------------------------------------
@router.get("/get_all_airline", status_code=status.HTTP_200_OK)
async def get_all_airline(request: Request):
    return await Classifier.get_all_airline(request)


@router.post("/create_airline", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airline(data: AirlineData, request: Request):
    return await Classifier.create_airline(data, request)


@router.put("/update_airline/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airline(field_id: int, data: AirlineData, request: Request):
    return await Classifier.update_airline(field_id, data, request)


@router.delete("/delete_airline/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airline(field_id: int, request: Request):
    return await Classifier.delete_airline(field_id, request)


# SCHEDULED_FLIGHT_MODEL -----------------------------------------------------------------------------------------
@router.get("/get_all_scheduled_flight_model", status_code=status.HTTP_200_OK)
async def get_all_scheduled_flight_model(request: Request):
    return await Classifier.get_all_scheduled_flight_model(request)


@router.post("/create_scheduled_flight_model", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_scheduled_flight_model(data: SchFlightModelData, request: Request):
    return await Classifier.create_scheduled_flight_model(data, request)


@router.put("/update_scheduled_flight_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_scheduled_flight_model(field_id: int, data: SchFlightModelData, request: Request):
    return await Classifier.update_scheduled_flight_model(field_id, data, request)


@router.delete("/delete_scheduled_flight_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_scheduled_flight_model(field_id: int, request: Request):
    return await Classifier.delete_scheduled_flight_model(field_id, request)


# AIRPLANE_MODEL -----------------------------------------------------------------------------------------------
@router.get("/get_all_airplane_model", status_code=status.HTTP_200_OK)
async def get_all_airplane_model(request: Request):
    return await Classifier.get_all_airplane_model(request)


@router.post("/create_airplane_model", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airplane_model(data: AirplaneModelData, request: Request):
    return await Classifier.create_airplane_model(data, request)


@router.put("/update_airplane_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airplane_model(field_id: int, data: AirplaneModelData, request: Request):
    return await Classifier.update_airplane_model(field_id, data, request)


@router.delete("/delete_airplane_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airplane_model(field_id: int, request: Request):
    return await Classifier.delete_airplane_model(field_id, request)


# AIRPLANE -----------------------------------------------------------------------------------------------
@router.get("/get_all_airplane", status_code=status.HTTP_200_OK)
async def get_all_airplane(request: Request):
    return await Classifier.get_all_airplane(request)


@router.post("/create_airplane", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airplane(data: AirplaneData, request: Request):
    return await Classifier.create_airplane(data, request)


@router.put("/update_airplane/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airplane(field_id: int, data: AirplaneData, request: Request):
    return await Classifier.update_airplane(field_id, data, request)


@router.delete("/delete_airplane/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airplane(field_id: int, request: Request):
    return await Classifier.delete_airplane(field_id, request)


# MAINTENANCE_MODEL -----------------------------------------------------------------------------------------------
@router.get("/get_all_maintenance_model", status_code=status.HTTP_200_OK)
async def get_all_maintenance_model(request: Request):
    return await Classifier.get_all_maintenance_model(request)


@router.post("/create_maintenance_model", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_maintenance_model(data: MaintenanceModelData, request: Request):
    return await Classifier.create_maintenance_model(data, request)


@router.put("/update_maintenance_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_maintenance_model(field_id: int, data: MaintenanceModelData, request: Request):
    return await Classifier.update_maintenance_model(field_id, data, request)


@router.delete("/delete_maintenance_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_maintenance_model(field_id: int, request: Request):
    return await Classifier.delete_maintenance_model(field_id, request)


# JOB_TITLE -----------------------------------------------------------------------------------------------
@router.get("/get_all_job_title", status_code=status.HTTP_200_OK)
async def get_all_job_title(request: Request):
    return await Classifier.get_all_job_title(request)


@router.post("/create_job_title", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_job_title(data: JobTitleData, request: Request):
    return await Classifier.create_job_title(data, request)


@router.put("/update_job_title/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_job_title(field_id: int, data: JobTitleData, request: Request):
    return await Classifier.update_job_title(field_id, data, request)


@router.delete("/delete_job_title/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_job_title(field_id: int, request: Request):
    return await Classifier.delete_job_title(field_id, request)


# EMPLOYEE -----------------------------------------------------------------------------------------------
@router.get("/get_all_employee", status_code=status.HTTP_200_OK)
async def get_all_employee(request: Request):
    return await Classifier.get_all_employee(request)


@router.post("/create_employee", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_employee(data: EmployeeData, request: Request):
    return await Classifier.create_employee(data, request)


@router.put("/update_employee/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_employee(field_id: int, data: EmployeeData, request: Request):
    return await Classifier.update_employee(field_id, data, request)


@router.delete("/delete_employee/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_employee(field_id: int, request: Request):
    return await Classifier.delete_employee(field_id, request)


# PRETRIP_MAINTENANCE -----------------------------------------------------------------------------------------------
@router.get("/get_all_pretrip_maintenance", status_code=status.HTTP_200_OK)
async def get_all_pretrip_maintenance(request: Request):
    return await Classifier.get_all_pretrip_maintenance(request)


@router.post("/create_pretrip_maintenance", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_pretrip_maintenance(data: PretripMaintenanceData, request: Request):
    return await Classifier.create_pretrip_maintenance(data, request)


@router.put("/update_pretrip_maintenance/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_pretrip_maintenance(field_id: int, data: PretripMaintenanceData, request: Request):
    return await Classifier.update_pretrip_maintenance(field_id, data, request)


@router.delete("/delete_pretrip_maintenance/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_pretrip_maintenance(field_id: int, request: Request):
    return await Classifier.delete_pretrip_maintenance(field_id, request)


# SCHEDULED_FLIGHT -----------------------------------------------------------------------------------------------
@router.get("/get_all_scheduled_flight", status_code=status.HTTP_200_OK)
async def get_all_scheduled_flight(request: Request):
    return await Classifier.get_all_scheduled_flight(request)


@router.post("/create_scheduled_flight", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_scheduled_flight(data: ScheduledFlightData, request: Request):
    return await Classifier.create_scheduled_flight(data, request)


@router.put("/update_scheduled_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_scheduled_flight(field_id: int, data: ScheduledFlightData, request: Request):
    return await Classifier.update_scheduled_flight(field_id, data, request)


@router.delete("/delete_scheduled_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_scheduled_flight(field_id: int, request: Request):
    return await Classifier.delete_scheduled_flight(field_id, request)
