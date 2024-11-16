from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Classifier:
    tables = ["country", "settlement", "airport", "airline", "airplane_model", "job_title", "scheduled_flight_model",
              "maintenance_model", "shop"]

    @classmethod
    def check_tablename(cls, tablename):
        if tablename not in Classifier.tables:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This classifier does not exist",
            )

    @classmethod
    async def create(cls, query: Query):
        Classifier.check_tablename(query.tablename)

        # check if admin

        return await Functions.create_field(query.tablename, query.args)

    """
    @classmethod
    async def get_by_id(cls, tablename: str, field_id: int):
        Classifier.check_tablename(tablename)

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
    async def get_by_name(cls, tablename: str, field_name: str):
        Classifier.check_tablename(tablename)

        querydb = select(Classifier.tablename[tablename]).filter_by(name=field_name)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This field does not exist",
            )
        return field
    """

    @classmethod
    async def get_all(cls, tablename: str):
        Classifier.check_tablename(tablename)
        return await Functions.get_all_from_table(tablename)

    @classmethod
    async def update(cls, field_id: int, query: Query):
        Classifier.check_tablename(query.tablename)

        # check if admin

        return await Functions.update_field(query.tablename, field_id, query.args.__dict__)

    @classmethod
    async def delete(cls, tablename: str, field_id: int):
        Classifier.check_tablename(tablename)

        # check if admin

        return await Functions.delete_field(tablename, field_id)
