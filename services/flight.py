from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Flight:
    tables = ["flight", "scheduled_flight", "airplane", "pretrip_maintenance"]

    @classmethod
    def check_tablename(cls, tablename):
        if tablename not in Flight.tables:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This table does not exist",
            )

    @classmethod
    async def create(cls, tablename: str, data: FlightInfo | ScheduledFlightInfo | AirplaneInfo | PretripMaintenanceInfo):
        Flight.check_tablename(tablename)

        # check if admin

        return await Functions.create_field(tablename, data.__dict__)

    @classmethod
    async def get_all(cls, tablename: str):
        Flight.check_tablename(tablename)
        return await Functions.get_all_from_table(tablename)

    @classmethod
    async def update(cls, tablename: str, field_id: int, data: FlightInfo | ScheduledFlightInfo | AirplaneInfo | PretripMaintenanceInfo):
        Flight.check_tablename(tablename)

        # check if admin

        return await Functions.update_field(tablename, field_id, data.__dict__)

    @classmethod
    async def delete(cls, tablename: str, field_id: int):
        Flight.check_tablename(tablename)

        # check if admin

        return await Functions.delete_field(tablename, field_id)
