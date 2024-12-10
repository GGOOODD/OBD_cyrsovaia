from fastapi import HTTPException, status, Request
from database import *
from schemas import *
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.exc import IntegrityError
from functions import Functions


class Classifier:
    # SHOP ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_shop(cls):
        return await Functions.get_all_from_table("shop")

    @classmethod
    async def create_shop(cls, data: ShopData):
        # check if admin
        return await Functions.create_field("shop", data.__dict__)

    @classmethod
    async def update_shop(cls, field_id: int, data: ShopData):
        # check if admin
        return await Functions.update_field("shop", field_id, data.__dict__)

    @classmethod
    async def delete_shop(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("shop", field_id)

    # COUNTRY ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_country(cls):
        # check if admin
        return await Functions.get_all_from_table("country")

    @classmethod
    async def create_country(cls, data: CountryData):
        # check if admin
        return await Functions.create_field("country", data.__dict__)

    @classmethod
    async def update_country(cls, field_id: int, data: CountryData):
        # check if admin
        return await Functions.update_field("country", field_id, data.__dict__)

    @classmethod
    async def delete_country(cls, field_id: id):
        # check if admin
        querydb = delete(SettlementModel).filter_by(country_id=field_id)
        async with new_session() as session:
            await session.execute(querydb)
            await session.commit()
        return await Functions.delete_field("country", field_id)

    # SETTLEMENT ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_settlement(cls):
        # check if admin
        querydb = select(SettlementModel).options(joinedload(SettlementModel.country))
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "name": field.name,
                         "countryName": field.country.name,
                         "settlementType": field.type})
        return data

    @classmethod
    async def create_settlement(cls, data: SettlementData):
        # check if admin
        querydb = select(CountryModel).filter_by(name=data.countryName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой страны не существует",
            )
        return await Functions.create_field("settlement",
                                            {"country_id": field.id,
                                             "name": data.name,
                                             "type": data.settlementType})

    @classmethod
    async def update_settlement(cls, field_id: int, data: SettlementData):
        # check if admin
        querydb = select(CountryModel).filter_by(name=data.countryName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой страны не существует",
            )
        return await Functions.update_field("settlement", field_id,
                                            {"country_id": field.id,
                                             "name": data.name,
                                             "type": data.settlementType})

    @classmethod
    async def delete_settlement(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("settlement", field_id)

    # AIRPORT ------------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airport(cls):
        # check if admin
        querydb = select(AirportModel).options(joinedload(AirportModel.settlement))
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "name": field.name,
                         "settlementName": field.settlement.name,
                         "address": field.address})
        return data

    @classmethod
    async def create_airport(cls, data: AirportData):
        # check if admin
        querydb = select(SettlementModel).filter_by(name=data.settlementName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого населённого пункта не существует",
            )
        return await Functions.create_field("airport",
                                            {"settlement_id": field.id,
                                             "name": data.name,
                                             "address": data.address})

    @classmethod
    async def update_airport(cls, field_id: int, data: AirportData):
        # check if admin
        querydb = select(SettlementModel).filter_by(name=data.settlementName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого населённого пункта не существует",
            )
        return await Functions.update_field("airport", field_id,
                                            {"settlement_id": field.id,
                                             "name": data.name,
                                             "address": data.address})

    @classmethod
    async def delete_airport(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("airport", field_id)

    # FLIGHT ------------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_flight(cls):
        # check if admin
        querydb = select(FlightModel).options(
            joinedload(FlightModel.airline),
            joinedload(FlightModel.airport)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "airlineName": field.airline.name,
                         "settlementName": field.airport.name})
        return data

    @classmethod
    async def create_flight(cls, data: FlightData):
        # check if admin
        querydb = select(AirlineModel).filter_by(name=data.airlineName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field1 = result.scalars().first()
        if field1 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой авиакомпании не существует",
            )

        querydb = select(AirportModel).filter_by(name=data.airportName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field2 = result.scalars().first()
        if field2 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого аэропорта не существует",
            )

        return await Functions.create_field("flight",
                                            {"airline_id": field1.id,
                                             "airport_id": field2.id})

    @classmethod
    async def update_flight(cls, field_id: int, data: FlightData):
        # check if admin
        querydb = select(AirlineModel).filter_by(name=data.airlineName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field1 = result.scalars().first()
        if field1 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой авиакомпании не существует",
            )

        querydb = select(AirportModel).filter_by(name=data.airportName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field2 = result.scalars().first()
        if field2 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого аэропорта не существует",
            )

        return await Functions.update_field("flight", field_id,
                                            {"airline_id": field1.id,
                                             "airport_id": field2.id})

    @classmethod
    async def delete_flight(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("flight", field_id)

    # AIRLINE ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airline(cls):
        # check if admin
        return await Functions.get_all_from_table("airline")

    @classmethod
    async def create_airline(cls, data: AirlineData):
        # check if admin
        return await Functions.create_field("airline", data.__dict__)

    @classmethod
    async def update_airline(cls, field_id: int, data: AirlineData):
        # check if admin
        return await Functions.update_field("airline", field_id, data.__dict__)

    @classmethod
    async def delete_airline(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("airline", field_id)

    # SCHEDULED_FLIGHT_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_scheduled_flight_model(cls):
        # check if admin
        return await Functions.get_all_from_table("scheduled_flight_model")

    @classmethod
    async def create_scheduled_flight_model(cls, data: SchFlightModelData):
        # check if admin
        return await Functions.create_field("scheduled_flight_model", data.__dict__)

    @classmethod
    async def update_scheduled_flight_model(cls, field_id: int, data: SchFlightModelData):
        # check if admin
        return await Functions.update_field("scheduled_flight_model", field_id, data.__dict__)

    @classmethod
    async def delete_scheduled_flight_model(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("scheduled_flight_model", field_id)

    # AIRPLANE_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airplane_model(cls):
        # check if admin
        return await Functions.get_all_from_table("airplane_model")

    @classmethod
    async def create_airplane_model(cls, data: AirplaneModelData):
        # check if admin
        return await Functions.create_field("airplane_model", data.__dict__)

    @classmethod
    async def update_airplane_model(cls, field_id: int, data: AirplaneModelData):
        # check if admin
        return await Functions.update_field("airplane_model", field_id, data.__dict__)

    @classmethod
    async def delete_airplane_model(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("airplane_model", field_id)

    # AIRPLANE_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airplane(cls):
        # check if admin
        querydb = select(AirplaneModel).options(joinedload(AirplaneModel.airplane_model))
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "airplaneModelName": field.airplane_model.name,
                         "registrationNumber": field.registration_number})
        return data

    @classmethod
    async def create_airplane(cls, data: AirplaneData):
        # check if admin
        querydb = select(AirplaneModelModel).filter_by(name=data.airplaneModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели самолёта не существует",
            )
        return await Functions.create_field("airplane",
                                            {"airplane_model_id": field.id,
                                             "registration_number": data.registrationNumber})

    @classmethod
    async def update_airplane(cls, field_id: int, data: AirplaneData):
        # check if admin
        querydb = select(AirplaneModelModel).filter_by(name=data.airplaneModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели самолёта не существует",
            )
        return await Functions.update_field("settlement", field_id,
                                            {"airplane_model_id": field.id,
                                             "registration_number": data.registrationNumber})

    @classmethod
    async def delete_airplane(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("airplane", field_id)

    # MAINTENANCE_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_maintenance_model(cls):
        # check if admin
        return await Functions.get_all_from_table("maintenance_model")

    @classmethod
    async def create_maintenance_model(cls, data: MaintenanceModelData):
        # check if admin
        return await Functions.create_field("maintenance_model", data.__dict__)

    @classmethod
    async def update_maintenance_model(cls, field_id: int, data: MaintenanceModelData):
        # check if admin
        return await Functions.update_field("maintenance_model", field_id, data.__dict__)

    @classmethod
    async def delete_maintenance_model(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("maintenance_model", field_id)

    # JOB_TITLE --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_job_title(cls):
        # check if admin
        return await Functions.get_all_from_table("job_title")

    @classmethod
    async def create_job_title(cls, data: JobTitleData):
        # check if admin
        return await Functions.create_field("job_title", data.__dict__)

    @classmethod
    async def update_job_title(cls, field_id: int, data: JobTitleData):
        # check if admin
        return await Functions.update_field("job_title", field_id, data.__dict__)

    @classmethod
    async def delete_job_title(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("job_title", field_id)

    # EMPLOYEE --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_employee(cls):
        # check if admin
        querydb = select(EmployeeModel).options(joinedload(EmployeeModel.job_title))
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "JobTitleName": field.job_title.name,
                         "surname": field.surname,
                         "name": field.name,
                         "patronymic": field.patronymic,
                         "experience": field.experience})
        return data

    @classmethod
    async def create_employee(cls, data: EmployeeData):
        # check if admin
        querydb = select(JobTitleModel).filter_by(name=data.jobTitleName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой должности не существует",
            )
        return await Functions.create_field("employee",
                                            {"job_title_id": field.id,
                                             "name": data.name,
                                             "surname": data.surname,
                                             "patronymic": data.patronymic,
                                             "experience": data.experience})

    @classmethod
    async def update_employee(cls, field_id: int, data: EmployeeData):
        # check if admin
        querydb = select(JobTitleModel).filter_by(name=data.jobTitleName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой должности не существует",
            )
        return await Functions.update_field("employee", field_id,
                                            {"job_title_id": field.id,
                                             "name": data.name,
                                             "surname": data.surname,
                                             "patronymic": data.patronymic,
                                             "experience": data.experience})

    @classmethod
    async def delete_employee(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("employee", field_id)

    # PRETRIP_MAINTENANCE --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_pretrip_maintenance(cls):
        # check if admin
        querydb = select(PretripMaintenanceModel).options(
            joinedload(PretripMaintenanceModel.maintenance_model),
            joinedload(PretripMaintenanceModel.employee),
            joinedload(PretripMaintenanceModel.airplane)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "maintenanceModelName": field.maintenance_model.name,
                         "surname": field.employee.surname,
                         "name": field.employee.name,
                         "patronymic": field.employee.patronymic,
                         "registrationNumber": field.airplane.registration_number,
                         "datetime": field.datetime.strftime('%d-%m-%Y %H:%M:%S'),
                         "result": field.result})
        return data

    @classmethod
    async def create_pretrip_maintenance(cls, data: PretripMaintenanceData):
        # check if admin
        querydb = select(MaintenanceModelModel).filter_by(name=data.maintenanceModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field1 = result.scalars().first()
        if field1 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели обслуживания не существует",
            )

        querydb = select(EmployeeModel).filter_by(name=data.name, surname=data.surname, patronymic=data.patronymic)
        async with new_session() as session:
            result = await session.execute(querydb)
        field2 = result.scalars().first()
        if field2 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого сотрудника не существует",
            )

        querydb = select(AirplaneModel).filter_by(registration_number=data.registrationNubmer)
        async with new_session() as session:
            result = await session.execute(querydb)
        field3 = result.scalars().first()
        if field3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого самолёта не существует",
            )
        return await Functions.create_field("pretrip_maintenance",
                                            {"maintenance_model_id": field1.id,
                                             "employee_id": field2.id,
                                             "airplane_id": field3.id,
                                             "datetime": datetime.strptime(data.datetime, '%d-%m-%Y %H:%M:%S'),
                                             "result": data.result})

    @classmethod
    async def update_pretrip_maintenance(cls, field_id: int, data: PretripMaintenanceData):
        # check if admin
        querydb = select(MaintenanceModelModel).filter_by(name=data.maintenanceModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field1 = result.scalars().first()
        if field1 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели обслуживания не существует",
            )

        querydb = select(EmployeeModel).filter_by(name=data.name, surname=data.surname, patronymic=data.patronymic)
        async with new_session() as session:
            result = await session.execute(querydb)
        field2 = result.scalars().first()
        if field2 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого сотрудника не существует",
            )

        querydb = select(AirplaneModel).filter_by(registration_number=data.registrationNubmer)
        async with new_session() as session:
            result = await session.execute(querydb)
        field3 = result.scalars().first()
        if field3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого самолёта не существует",
            )
        return await Functions.update_field("pretrip_maintenance", field_id,
                                            {"maintenance_model_id": field1.id,
                                             "employee_id": field2.id,
                                             "airplane_id": field3.id,
                                             "datetime": datetime.strptime(data.datetime, '%d-%m-%Y %H:%M:%S'),
                                             "result": data.result})

    @classmethod
    async def delete_pretrip_maintenance(cls, field_id: id):
        # check if admin
        return await Functions.delete_field("pretrip_maintenance", field_id)

    # SCHEDULED_FLIGHT --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_scheduled_flight(cls):
        # check if admin
        querydb = select(ScheduledFlightModel).options(
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airline),
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airport),
            joinedload(ScheduledFlightModel.airplane),
            joinedload(ScheduledFlightModel.scheduled_flight_model)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "airlineName": field.flight.airline.name,
                         "airportName": field.flight.airport.name,
                         "datetimeDeparture": field.departure_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                         "datetimeArrival": field.arrival_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                         "registrationNumber": field.airplane.registration_number,
                         "scheduledFlightModelName": field.scheduled_flight_model.name})
        return data

    @classmethod
    async def create_scheduled_flight(cls, data: ScheduledFlightData):
        # check if admin
        querydb = select(FlightModel).join(FlightModel.airport).join(FlightModel.airline).options(
            contains_eager(FlightModel.airline),
            contains_eager(FlightModel.airport)
        ).filter(and_(
            AirlineModel.name == data.airlineName,
            AirportModel.name == data.airportName)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        field1 = result.scalars().first()
        if field1 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого рейса не существует",
            )

        querydb = select(AirplaneModel).filter_by(registration_number=data.registrationNumber)
        async with new_session() as session:
            result = await session.execute(querydb)
        field2 = result.scalars().first()
        if field2 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого самолёта не существует",
            )

        querydb = select(ScheduledFlightModelModel).filter_by(name=data.scheduledFlightModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field3 = result.scalars().first()
        if field3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели назначенного рейса не существует",
            )
        inform = await Functions.create_field("scheduled_flight",
                                              {"flight_id": field1.id,
                                               "airplane_id": field2.id,
                                               "scheduled_flight_model_id": field3.id,
                                               "departure_datetime": datetime.strptime(data.datetimeDeparture, '%d-%m-%Y %H:%M:%S'),
                                               "arrival_datetime": datetime.strptime(data.datetimeArrival, '%d-%m-%Y %H:%M:%S')})

        #async with new_session() as session:
        for employee_id in data.crew:
            await Functions.create_field("crew",
                                         {"scheduled_flight_id": inform.field_id,
                                          "employee_id": employee_id})
            # crew = CrewModel(scheduled_flight_id=inform.field_id, employee_id=employee_id)
            # session.add(crew)
            # session.commit()
            # await Functions.check_foreign_keys()
        return Inform(detail="created", field_id=inform.field_id)

    @classmethod
    async def update_scheduled_flight(cls, field_id: int, data: ScheduledFlightData):
        # check if admin
        querydb = select(FlightModel).options(
            joinedload(FlightModel.airline),
            joinedload(FlightModel.airport)
        ).filter(
            AirlineModel.name == data.airlineName,
            AirportModel.name == data.airportName
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        field1 = result.scalars().first()
        if field1 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого рейса не существует",
            )

        querydb = select(AirplaneModel).filter_by(registration_number=data.registrationNubmer)
        async with new_session() as session:
            result = await session.execute(querydb)
        field2 = result.scalars().first()
        if field2 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого самолёта не существует",
            )

        querydb = select(ScheduledFlightModelModel).filter_by(name=data.scheduledFlightModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field3 = result.scalars().first()
        if field3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели назначенного рейса не существует",
            )
        inform = await Functions.update_field("scheduled_flight", field_id,
                                              {"flight_id": field1.id,
                                               "airplane_id": field2.id,
                                               "scheduled_flight_model_id": field3.id,
                                               "departure_datetime": datetime.strptime(data.datetimeDeparture, '%d-%m-%Y %H:%M:%S'),
                                               "arrival_datetime": datetime.strptime(data.datetimeArrival, '%d-%m-%Y %H:%M:%S')})

        querydb = delete(CrewModel).filter_by(scheduled_flight_id=inform.field_id)
        #async with new_session() as session:
        await session.execute(querydb)
        for employee_id in data.crew:
            await Functions.create_field("crew",
                                         {"scheduled_flight_id": inform.field_id,
                                          "employee_id": employee_id})
            #crew = CrewModel(scheduled_flight_id=inform.field_id, employee_id=employee_id)
            #session.add(crew)
            #await session.commit()
            #await Functions.check_foreign_keys()
        return Inform(detail="created", field_id=None)

    @classmethod
    async def delete_scheduled_flight(cls, field_id: id):
        # check if admin
        querydb = delete(CrewModel).filter_by(scheduled_flight_id=field_id)
        async with new_session() as session:
            await session.execute(querydb)
            await session.commit()
        return await Functions.delete_field("scheduled_flight", field_id)
