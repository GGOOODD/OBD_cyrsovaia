from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from services import Auth
import jwt
import sqlite3


class Functions:
    tablename = {"country": CountryModel, "settlement": SettlementModel, "airport": AirportModel, "airline": AirlineModel,
                 "airplane_model": AirplaneModelModel, "job_title": JobTitleModel, "scheduled_flight_model": ScheduledFlightModelModel,
                 "maintenance_model": MaintenanceModelModel, "shop": ShopModel, "flight": FlightModel,
                 "scheduled_flight": ScheduledFlightModel, "airplane": AirplaneModel, "pretrip_maintenance": PretripMaintenanceModel,
                 "user": UserModel, "flight_history": FlightHistoryModel, "employee": EmployeeModel, "crew": CrewModel}

    @classmethod
    async def get_user_id(cls, request: Request) -> int:
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login cookie was not found",
            )
        cookie = jwt.decode(token, Auth.key, Auth.algorithm)
        query = select(UserModel).filter_by(id=cookie["id"])
        async with new_session() as session:
            result = await session.execute(query)
        user_field = result.scalars().first()
        if user_field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User cookie is outdated"
            )

        return user_field.id

    @classmethod
    async def check_foreign_keys(cls):
        conn = sqlite3.connect('site.db')
        cursor = conn.execute("PRAGMA foreign_key_check;")
        violations = cursor.fetchall()
        conn.close()
        if violations:
            async with new_session() as session:
                try:
                    querydb = delete(Functions.tablename[violations[0][0]]).filter_by(id=violations[0][1])
                except InvalidRequestError:
                    querydb = delete(Functions.tablename[violations[0][0]]).filter_by(employee_id=violations[0][1])
                await session.execute(querydb)
                await session.flush()
                await session.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key is wrong"
            )

    @classmethod
    def check_tablename(cls, tablename: str):
        try:
            Functions.tablename[tablename]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tablename does not exist",
            )

    @classmethod
    async def create_field(cls, tablename: str, args: dict):
        Functions.check_tablename(tablename)
        try:
            query_field = Functions.tablename[tablename](**args)
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Args is wrong",
            )

        async with new_session() as session:
            session.add(query_field)
            try:
                await session.flush()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Args is wrong",
                )
            await session.commit()
            # await Functions.check_foreign_keys()
        if tablename == "crew":
            return Inform(detail="created", field_id=None)
        return Inform(detail="created", field_id=query_field.id)

    @classmethod
    async def get_all_from_table(cls, tablename: str):
        Functions.check_tablename(tablename)

        querydb = select(Functions.tablename[tablename])
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        return fields

    @classmethod
    async def update_field(cls, tablename: str, field_id: int, args: dict):
        Functions.check_tablename(tablename)

        querydb = select(Functions.tablename[tablename]).filter_by(id=field_id)
        async with new_session() as session:
            result = await session.execute(querydb)
            field = result.scalars().first()
            if field is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This field does not exist",
                )
            for key, value in args.items():
                setattr(field, key, value)

            try:
                await session.flush()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Args is wrong",
                )
            await session.commit()
            # await Functions.check_foreign_keys()
        return Inform(detail="updated", field_id=None)

    @classmethod
    async def delete_field(cls, tablename: str, field_id: int):
        Functions.check_tablename(tablename)

        querydb = select(Functions.tablename[tablename]).filter_by(id=field_id)
        async with new_session() as session:
            result = await session.execute(querydb)
            field = result.scalars().first()
            if field is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This field does not exist",
                )
            querydb = delete(Functions.tablename[tablename]).filter_by(id=field_id)
            await session.execute(querydb)
            await session.flush()
            await session.commit()
        return Inform(detail="field deleted", field_id=None)
