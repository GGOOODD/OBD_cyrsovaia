from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Employee:
    tables = ["employee", "crew"]

    @classmethod
    def check_tablename(cls, tablename):
        if tablename not in Employee.tables:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This table does not exist",
            )

    @classmethod
    async def create(cls, tablename: str, data: EmployeeInfo | CrewInfo):
        Employee.check_tablename(tablename)

        # check if admin

        return await Functions.create_field(tablename, data.__dict__)

    @classmethod
    async def get_all(cls, tablename: str):
        Employee.check_tablename(tablename)

        # check if admin

        return await Functions.get_all_from_table(tablename)

    @classmethod
    async def get_flight_crew_by_flight_id(cls, flight_id: int):

        # check if admin

        querydb = select(CrewModel).filter_by(flight_id=flight_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        return fields

    @classmethod
    async def get_flight_crew_by_employee_id(cls, employee_id: int):

        # check if admin

        querydb = select(CrewModel).filter_by(flight_id=employee_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()

        return field

    @classmethod
    async def delete(cls, tablename: str, field_id: int):
        Employee.check_tablename(tablename)

        # check if admin

        return await Functions.delete_field(tablename, field_id)