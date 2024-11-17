from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class User:
    tables = ["flight_history"]

    @classmethod
    def check_tablename(cls, tablename):
        if tablename not in User.tables:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This table does not exist",
            )

    @classmethod
    async def create(cls, tablename: str, data: FlightHistoryInfo, request: Request):
        User.check_tablename(tablename)

        # check if user, add user_id in data
        user_id = await Functions.get_user_id(request)
        data.__dict__["user_id"] = user_id

        return await Functions.create_field(tablename, data.__dict__)

    @classmethod
    async def get_all(cls, tablename: str, request: Request):
        User.check_tablename(tablename)

        # check if user, get user_id
        user_id = await Functions.get_user_id(request)

        querydb = select(Functions.tablename[tablename]).filter_by(user_id=user_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        return fields
