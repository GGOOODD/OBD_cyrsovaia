from fastapi import APIRouter, status, Request
from schemas import *
from services import User

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/create_flight_history/{sch_flight_id}", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_flight_histiory(sch_flight_id: int, request: Request):
    return await User.create_flight_history(sch_flight_id, request)


@router.get("/get_all_flight_history", status_code=status.HTTP_200_OK)
async def get_all_flight_history(request: Request):
    return await User.get_all_flight_history(request)


@router.get("/get_user_info", status_code=status.HTTP_200_OK)
async def get_user_info(request: Request):
    return await User.get_user_info(request)


@router.put("/change_password", response_model=Inform, status_code=status.HTTP_200_OK)
async def change_password(password: UpdPassword, request: Request):
    return await User.change_password(password, request)


@router.put("/change_fio", response_model=Inform, status_code=status.HTTP_200_OK)
async def change_fio(fio: UpdFIO, request: Request):
    return await User.change_fio(fio, request)
