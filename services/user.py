from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from functions import Functions
import jwt
from services import Auth


class User:
    @classmethod
    async def create_flight_history(cls, sch_flight_id: int, request: Request):
        user_id = await Functions.get_user_id(request)

        querydb = select(FlightHistoryModel).filter_by(user_id=user_id, scheduled_flight_id=sch_flight_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is not None:
            return Inform(detail="Вы уже купили билет на данный рейс", field_id=None)

        now = datetime.strptime(datetime.now().strftime('%d-%m-%Y %H:%M'), '%d-%m-%Y %H:%M')
        querydb = select(FlightHistoryModel).filter_by(scheduled_flight_id=sch_flight_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()
        for literal in "ABCDEF":
            for number in range(1, 28):
                gen_seat = literal + str(number)
                flag = True
                for field in fields:
                    if field.seat == gen_seat:
                        flag = False
                        break
                if flag:
                    await Functions.create_field("flight_history",
                                                 {"user_id": user_id,
                                                  "scheduled_flight_id": sch_flight_id,
                                                  "payment_datetime": now,
                                                  "seat": gen_seat})
                    return Inform(detail="Билет успешно куплен, информацию о нём можно найти в истории рейсов", field_id=None)
        return Inform(detail="Все билеты уже выкуплены", field_id=None)

    @classmethod
    async def get_all_flight_history(cls, request: Request):
        # check if user, get user_id
        user_id = await Functions.get_user_id(request)

        querydb = select(FlightHistoryModel).filter_by(user_id=user_id).options(
            joinedload(FlightHistoryModel.scheduled_flight)
            .joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airline),
            joinedload(FlightHistoryModel.scheduled_flight)
            .joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airport)
            .joinedload(AirportModel.settlement)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"airline": field.scheduled_flight.flight.airline.name,
                         "destination": field.scheduled_flight.flight.airport.settlement.name,
                         "airport": field.scheduled_flight.flight.airport.name,
                         "payment_datetime": field.payment_datetime.strftime('%d-%m-%Y %H:%M'),
                         "seat": field.seat})
        return data

    @classmethod
    async def get_user_info(cls, request: Request):
        # check if user, get user_id
        user_id = await Functions.get_user_id(request)

        querydb = select(UserModel).filter_by(id=user_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()

        data = {"name": field.name, "surname": field.surname, "patronymic": field.patronymic, "email": field.email}
        return data

    @classmethod
    async def change_password(cls, password: UpdPassword, request: Request):
        user_id = await Functions.get_user_id(request)

        querydb = select(UserModel).filter_by(id=user_id)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()

        field.password = jwt.encode({"password": password.password}, Auth.key, Auth.algorithm)
        try:
            await session.flush()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Args is wrong",
            )
        await session.commit()
        return Inform(detail="done", field_id=None)

    @classmethod
    async def change_fio(cls, fio: UpdFIO, request: Request):
        user_id = await Functions.get_user_id(request)

        return await Functions.update_field("user", user_id, fio.__dict__)
