from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Flight:

    @classmethod
    async def create_scheduled_flight(cls, info: ScheduledFlightInfo):

        # check if admin

        #return await Functions.create_field(tablename, data.__dict__)
        return

    @classmethod
    async def get_all_scheduled_flight(cls):
        querydb = select(ScheduledFlightModel).options(
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airport)
            .joinedload(AirportModel.settlement)
            .joinedload(SettlementModel.country)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "country": field.flight.airport.settlement.country.name,
                         "destination": field.flight.airport.settlement.name,
                         "airport": field.flight.airport.name,
                         "departure": field.departure_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                         "arrival": field.arrival_datetime.strftime('%d-%m-%Y %H:%M:%S')})

        return data

    @classmethod
    async def get_scheduled_flight(cls, field_id):
        querydb = select(ScheduledFlightModel).filter_by(id=field_id).options(
            joinedload(ScheduledFlightModel.scheduled_flight_model),
            joinedload(ScheduledFlightModel.airplane)
            .joinedload(AirplaneModel.airplane_model),
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airline),
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airport)
            .joinedload(AirportModel.settlement)
            .joinedload(SettlementModel.country)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()

        if field is None:
            return Inform(detail="Такого назначенного рейса не существует", field_id=None)

        data = {"airline": field.flight.airline.name,
                "country": field.flight.airport.settlement.country.name,
                "destination": field.flight.airport.settlement.name,
                "airport": field.flight.airport.name,
                "departure": field.departure_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                "arrival": field.arrival_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                "airplane": field.airplane.airplane_model.name,
                "scheduled_flight_model": field.scheduled_flight_model.name,
                "crew": []}

        querydb = select(CrewModel).filter_by(scheduled_flight_id=field_id).options(
            joinedload(CrewModel.employee)
            .joinedload(EmployeeModel.job_title)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        for fieldi in fields:
            data["crew"].append({"name": fieldi.employee.name,
                                 "surname": fieldi.employee.surname,
                                 "patronymic": fieldi.employee.patronymic,
                                 "job_title": fieldi.employee.job_title.name})

        return data



    @classmethod
    async def update_scheduled_flight(cls, field_id: int, info: ScheduledFlightInfo):

        # check if admin

        return await Functions.update_field("scheduled_flight", field_id, info.__dict__)

    @classmethod
    async def delete__scheduled_flight(cls, field_id: int):

        # check if admin

        return await Functions.delete_field("scheduled_flight", field_id)
