from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Classifier:

    tablename = {"country": CountryModel, "settlement": SettlementModel, "airport": AirportModel, "airline": AirlineModel,
                 "airplane_model": AirplaneModelModel, "job_title": JobTitleModel, "scheduled_flight_model": ScheduledFlightModelModel,
                 "maintenance_model": MaintenanceModelModel, "shop": ShopModel}
    @classmethod
    async def create(cls, query: Query):
        try:
            Classifier.tablename[query.tablename]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tablename does not exist",
            )

        query_field = Classifier.tablename[query.tablename](**query.args)
        async with new_session() as session:
            session.add(query_field)
            try:
                await session.flush()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Args is wrong",
                )
            await session.commit()
        return Inform(detail="created")

    @classmethod
    async def get(cls, tablename: str, field_id: int):
        try:
            Classifier.tablename[tablename]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tablename does not exist",
            )

        querydb = select(Classifier.tablename[tablename]).filter_by(id=field_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This field does not exist",
            )
        return field

    @classmethod
    async def get_all(cls, tablename: str):
        try:
            Classifier.tablename[tablename]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tablename does not exist",
            )

        querydb = select(Classifier.tablename[tablename])
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        return fields

    @classmethod
    async def update(cls, field_id: int, query: Query):
        try:
            Classifier.tablename[query.tablename]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tablename does not exist",
            )

        querydb = select(Classifier.tablename[query.tablename]).filter_by(id=field_id)
        async with new_session() as session:
            result = await session.execute(querydb)
            field = result.scalars().first()
            if field is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This field does not exist",
                )
            for key, value in query.args.items():
                setattr(field, key, value)

            try:
                await session.flush()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Args is wrong",
                )
            await session.commit()
        return Inform(detail="updated")


    @classmethod
    async def delete(cls, tablename: str, field_id: int):
        try:
            Classifier.tablename[tablename]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tablename does not exist",
            )

        querydb = select(Classifier.tablename[tablename]).filter_by(id=field_id)
        async with new_session() as session:
            result = await session.execute(querydb)
            field = result.scalars().first()
            if field is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This field does not exist",
                )
            querydb = delete(Classifier.tablename[tablename]).filter_by(id=field_id)
            await session.execute(querydb)
            await session.flush()
            await session.commit()
        return Inform(detail="task deleted")
