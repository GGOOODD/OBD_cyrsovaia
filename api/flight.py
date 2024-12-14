from fastapi import APIRouter, status, Request
from schemas import *
from services import Flight

router = APIRouter(tags=["Flight"], prefix="/flight")


@router.get("/get_all_scheduled_flight", status_code=status.HTTP_200_OK)
async def get_all_scheduled_flight():
    return await Flight.get_all_scheduled_flight()


@router.get("/get_scheduled_flight/{field_id}", status_code=status.HTTP_200_OK)
async def get_scheduled_flight(field_id: int):
    return await Flight.get_scheduled_flight(field_id)

