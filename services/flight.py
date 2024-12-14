from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Flight:
    @classmethod
    async def get_all_scheduled_flight(cls):
        current_time = datetime.now()
        querydb = select(ScheduledFlightModel).options(
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airport)
            .joinedload(AirportModel.settlement)
            .joinedload(SettlementModel.country)
        ).where(ScheduledFlightModel.departure_datetime > current_time)
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "country": field.flight.airport.settlement.country.name,
                         "destination": field.flight.airport.settlement.name,
                         "airport": field.flight.airport.name,
                         "departure": field.departure_datetime.strftime('%d-%m-%Y %H:%M'),
                         "arrival": field.arrival_datetime.strftime('%d-%m-%Y %H:%M')})

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
                "departure": field.departure_datetime.strftime('%d-%m-%Y %H:%M'),
                "arrival": field.arrival_datetime.strftime('%d-%m-%Y %H:%M'),
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
