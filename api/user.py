from fastapi import APIRouter, status, Request
from schemas import *
from services import User

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/create_flight_history", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_flight_histiory(data: FlightHistoryInfo, request: Request):
    return await User.create("flight_history", data, request)


@router.get("/get_all_flight_history", response_model=list[GetFlightHistory], status_code=status.HTTP_200_OK)
async def get_all_flight_history(request: Request):
    return await User.get_all("flight_history", request)
