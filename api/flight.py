from fastapi import APIRouter, status, Request
from schemas import *
from services import Flight

router = APIRouter(tags=["Flight"], prefix="/flight")

"""
@router.post("/create_flight", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_flight(data: FlightInfo):
    return await Flight.create("flight", data)


@router.post("/create_scheduled_flight", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_scheduled_flight(data: ScheduledFlightInfo):
    return await Flight.create("scheduled_flight", data)


@router.post("/create_airplane", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_airplane(data: AirplaneInfo):
    return await Flight.create("airplane", data)


@router.post("/create_pretrip_maintenance", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_pretrip_maintenance(data: PretripMaintenanceInfo):
    return await Flight.create("pretrip_maintenance", data)
"""

@router.get("/get_all_scheduled_flight", status_code=status.HTTP_200_OK)
async def get_all_scheduled_flight():
    return await Flight.get_all_scheduled_flight()


@router.get("/get_scheduled_flight/{field_id}", status_code=status.HTTP_200_OK)
async def get_scheduled_flight(field_id: int):
    return await Flight.get_scheduled_flight(field_id)

"""
@router.put("/update_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_flight(field_id: int, data: FlightInfo):
    return await Flight.update("flight", field_id, data)


@router.put("/update_scheduled_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_scheduled_flight(field_id: int, data: ScheduledFlightInfo):
    return await Flight.update("scheduled_flight", field_id, data)


@router.put("/update_airplane/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_airplane(field_id: int, data: AirplaneInfo):
    return await Flight.update("airplane", field_id, data)


@router.put("/update_pretrip_maintenance/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_pretrip_maintenance(field_id: int, data: PretripMaintenanceInfo):
    return await Flight.update("pretrip_maintenance", field_id, data)


@router.delete("/delete_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_flight(field_id: int):
    return await Flight.delete("flight", field_id)


@router.delete("/delete_scheduled_flight/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_scheduled_flight(field_id: int):
    return await Flight.delete("scheduled_flight", field_id)


@router.delete("/delete_airplane/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_airplane(field_id: int):
    return await Flight.delete("airplane", field_id)


@router.delete("/delete_pretrip_maintenance/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_pretrip_maintenance(field_id: int):
    return await Flight.delete("pretrip_maintenance", field_id)
"""
