from fastapi import APIRouter, status, Request
from schemas import *
from services import Classifier

router = APIRouter(tags=["Classifier"], prefix="/classifier")


# SHOP -----------------------------------------------------------------------------------------------------------
@router.get("/get_all_shop", status_code=status.HTTP_200_OK)
async def get_all_shop():
    return await Classifier.get_all_shop()


@router.post("/create_shop", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_shop(data: ShopData):
    return await Classifier.create_shop(data)


@router.put("/update_shop/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_shop(field_id: int, data: ShopData):
    return await Classifier.update_shop(field_id, data)


@router.delete("/delete_shop/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_shop(field_id: int):
    return await Classifier.delete_shop(field_id)


# COUNTRY ---------------------------------------------------------------------------------------------------------
@router.get("/get_all_country", status_code=status.HTTP_200_OK)
async def get_all_country():
    return await Classifier.get_all_country()


@router.post("/create_country", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_country(data: CountryData):
    return await Classifier.create_country(data)


@router.put("/update_country/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_country(field_id: int, data: CountryData):
    return await Classifier.update_country(field_id, data)


@router.delete("/delete_country/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_country(field_id: int):
    return await Classifier.delete_country(field_id)


# SETTLEMENT ------------------------------------------------------------------------------------------------------
@router.get("/get_all_settlement", status_code=status.HTTP_200_OK)
async def get_all_settlement():
    return await Classifier.get_all_settlement()


@router.post("/create_settlement", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_settlement(data: SettlementData):
    return await Classifier.create_settlement(data)


@router.put("/update_settlement/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_settlement(field_id: int, data: SettlementData):
    return await Classifier.update_settlement(field_id, data)


@router.delete("/delete_settlement/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_settlement(field_id: int):
    return await Classifier.delete_settlement(field_id)


# AIRPORT ------------------------------------------------------------------------------------------------------
@router.get("/get_all_airport", status_code=status.HTTP_200_OK)
async def get_all_airport():
    return await Classifier.get_all_airport()


@router.post("/create_airport", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airport(data: AirportData):
    return await Classifier.create_airport(data)


@router.put("/update_airport/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airport(field_id: int, data: AirportData):
    return await Classifier.update_airport(field_id, data)


@router.delete("/delete_airport/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airport(field_id: int):
    return await Classifier.delete_airport(field_id)


# FLIGHT --------------------------------------------------------------------------------------------------------
@router.get("/get_all_flight", status_code=status.HTTP_200_OK)
async def get_all_flight():
    return await Classifier.get_all_flight()


@router.post("/create_flight", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_flight(data: FlightData):
    return await Classifier.create_flight(data)


@router.put("/update_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_flight(field_id: int, data: FlightData):
    return await Classifier.update_flight(field_id, data)


@router.delete("/delete_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_flight(field_id: int):
    return await Classifier.delete_flight(field_id)


# AIRLINE --------------------------------------------------------------------------------------------------------
@router.get("/get_all_airline", status_code=status.HTTP_200_OK)
async def get_all_airline():
    return await Classifier.get_all_airline()


@router.post("/create_airline", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airline(data: AirlineData):
    return await Classifier.create_airline(data)


@router.put("/update_airline/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airline(field_id: int, data: AirlineData):
    return await Classifier.update_airline(field_id, data)


@router.delete("/delete_airline/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airline(field_id: int):
    return await Classifier.delete_airline(field_id)


# SCHEDULED_FLIGHT_MODEL -----------------------------------------------------------------------------------------
@router.get("/get_all_sch_flight_model", status_code=status.HTTP_200_OK)
async def get_all_sch_flight_model():
    return await Classifier.get_all_sch_flight_model()


@router.post("/create_sch_flight_model", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_sch_flight_model(data: SchFlightModelData):
    return await Classifier.create_sch_flight_model(data)


@router.put("/update_sch_flight_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_sch_flight_model(field_id: int, data: SchFlightModelData):
    return await Classifier.update_sch_flight_model(field_id, data)


@router.delete("/delete_sch_flight_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_sch_flight_model(field_id: int):
    return await Classifier.delete_sch_flight_model(field_id)


# AIRPLANE_MODEL -----------------------------------------------------------------------------------------------
@router.get("/get_all_airplane_model", status_code=status.HTTP_200_OK)
async def get_all_airplane_model():
    return await Classifier.get_all_airplane_model()


@router.post("/create_airplane_model", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airplane_model(data: AirplaneModelData):
    return await Classifier.create_airplane_model(data)


@router.put("/update_airplane_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airplane_model(field_id: int, data: AirplaneModelData):
    return await Classifier.update_airplane_model(field_id, data)


@router.delete("/delete_airplane_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airplane_model(field_id: int):
    return await Classifier.delete_airplane_model(field_id)


# AIRPLANE -----------------------------------------------------------------------------------------------
@router.get("/get_all_airplane", status_code=status.HTTP_200_OK)
async def get_all_airplane():
    return await Classifier.get_all_airplane()


@router.post("/create_airplane", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airplane(data: AirplaneData):
    return await Classifier.create_airplane(data)


@router.put("/update_airplane/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airplane(field_id: int, data: AirplaneData):
    return await Classifier.update_airplane(field_id, data)


@router.delete("/delete_airplane/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airplane(field_id: int):
    return await Classifier.delete_airplane(field_id)


# MAINTENANCE_MODEL -----------------------------------------------------------------------------------------------
@router.get("/get_all_maintenance_model", status_code=status.HTTP_200_OK)
async def get_all_maintenance_model():
    return await Classifier.get_all_maintenance_model()


@router.post("/create_maintenance_model", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_maintenance_model(data: MaintenanceModelData):
    return await Classifier.create_maintenance_model(data)


@router.put("/update_maintenance_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_maintenance_model(field_id: int, data: MaintenanceModelData):
    return await Classifier.update_maintenance_model(field_id, data)


@router.delete("/delete_maintenance_model/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_maintenance_model(field_id: int):
    return await Classifier.delete_maintenance_model(field_id)


# JOB_TITLE -----------------------------------------------------------------------------------------------
@router.get("/get_all_job_title", status_code=status.HTTP_200_OK)
async def get_all_job_title():
    return await Classifier.get_all_job_title()


@router.post("/create_job_title", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_job_title(data: JobTitleData):
    return await Classifier.create_job_title(data)


@router.put("/update_job_title/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_job_title(field_id: int, data: JobTitleData):
    return await Classifier.update_job_title(field_id, data)


@router.delete("/delete_job_title/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_job_title(field_id: int):
    return await Classifier.delete_job_title(field_id)


# EMPLOYEE -----------------------------------------------------------------------------------------------
@router.get("/get_all_employee", status_code=status.HTTP_200_OK)
async def get_all_employee():
    return await Classifier.get_all_employee()


@router.post("/create_employee", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_employee(data: EmployeeData):
    return await Classifier.create_employee(data)


@router.put("/update_employee/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_employee(field_id: int, data: EmployeeData):
    return await Classifier.update_employee(field_id, data)


@router.delete("/delete_employee/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_employee(field_id: int):
    return await Classifier.delete_employee(field_id)


# PRETRIP_MAINTENANCE -----------------------------------------------------------------------------------------------
@router.get("/get_all_pretrip_maintenance", status_code=status.HTTP_200_OK)
async def get_all_pretrip_maintenance():
    return await Classifier.get_all_pretrip_maintenance()


@router.post("/create_pretrip_maintenance", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_pretrip_maintenance(data: PretripMaintenanceData):
    return await Classifier.create_pretrip_maintenance(data)


@router.put("/update_pretrip_maintenance/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_pretrip_maintenance(field_id: int, data: PretripMaintenanceData):
    return await Classifier.update_pretrip_maintenance(field_id, data)


@router.delete("/delete_pretrip_maintenance/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_pretrip_maintenance(field_id: int):
    return await Classifier.delete_pretrip_maintenance(field_id)


# SCHEDULED_FLIGHT -----------------------------------------------------------------------------------------------
@router.get("/get_all_scheduled_flight", status_code=status.HTTP_200_OK)
async def get_all_scheduled_flight():
    return await Classifier.get_all_scheduled_flight()


@router.post("/create_scheduled_flight", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_scheduled_flight(data: ScheduledFlightData):
    return await Classifier.create_scheduled_flight(data)


@router.put("/update_scheduled_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_scheduled_flight(field_id: int, data: ScheduledFlightData):
    return await Classifier.update_scheduled_flight(field_id, data)


@router.delete("/delete_scheduled_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_scheduled_flight(field_id: int):
    return await Classifier.delete_scheduled_flight(field_id)
