from fastapi import APIRouter, status, Request
from schemas import *
from services import Employee

router = APIRouter(tags=["Employee"], prefix="/employee")


@router.post("/add_employee", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def add_employee(data: EmployeeInfo):
    return await Employee.create("employee", data)


@router.post("/asign_employee_on_flight", response_model=Inform, status_code=status.HTTP_200_OK)
async def asign_employee_on_flight(data: CrewInfo):
    return await Employee.create("crew", data)


@router.get("/get_all_employee", response_model=list[GetEmployee], status_code=status.HTTP_200_OK)
async def get_all_employee():
    return await Employee.get_all("employee")


@router.get("/get_flight_crew_by_flight_id/{flight_id}", response_model=list[GetCrew], status_code=status.HTTP_200_OK)
async def get_flight_crew_by_flight_id(flight_id: int):
    return await Employee.get_flight_crew_by_flight_id(flight_id)


@router.get("/get_flight_crew_by_employee_id/{employee_id}", response_model=GetCrew, status_code=status.HTTP_200_OK)
async def get_flight_crew_by_employee_id(employee_id: int):
    return await Employee.get_flight_crew_by_employee_id(employee_id)


@router.delete("/delete_employee/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_employee(field_id: int):
    return await Employee.delete("employee", field_id)


@router.delete("/delete_crew/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_crew(field_id: int):
    return await Employee.delete("crew", field_id)
