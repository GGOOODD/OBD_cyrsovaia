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
    async def create_shop(cls, data: ShopData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("shop", data.__dict__)

    @classmethod
    async def update_shop(cls, field_id: int, data: ShopData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("shop", field_id, data.__dict__)

    @classmethod
    async def delete_shop(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("shop", field_id)

    # COUNTRY ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_country(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.get_all_from_table("country")

    @classmethod
    async def create_country(cls, data: CountryData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("country", data.__dict__)

    @classmethod
    async def update_country(cls, field_id: int, data: CountryData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("country", field_id, data.__dict__)

    @classmethod
    async def delete_country(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        querydb = delete(SettlementModel).filter_by(country_id=field_id)
        async with new_session() as session:
            await session.execute(querydb)
            await session.commit()
        return await Functions.delete_field("country", field_id)

    # SETTLEMENT ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_settlement(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def create_settlement(cls, data: SettlementData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def update_settlement(cls, field_id: int, data: SettlementData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def delete_settlement(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("settlement", field_id)

    # AIRPORT ------------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airport(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def create_airport(cls, data: AirportData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def update_airport(cls, field_id: int, data: AirportData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def delete_airport(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("airport", field_id)

    # FLIGHT ------------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_flight(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
                         "airportName": field.airport.name})
        return data

    @classmethod
    async def create_flight(cls, data: FlightData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def update_flight(cls, field_id: int, data: FlightData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def delete_flight(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("flight", field_id)

    # AIRLINE ----------------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airline(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.get_all_from_table("airline")

    @classmethod
    async def create_airline(cls, data: AirlineData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("airline", data.__dict__)

    @classmethod
    async def update_airline(cls, field_id: int, data: AirlineData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("airline", field_id, data.__dict__)

    @classmethod
    async def delete_airline(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("airline", field_id)

    # SCHEDULED_FLIGHT_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_scheduled_flight_model(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.get_all_from_table("scheduled_flight_model")

    @classmethod
    async def create_scheduled_flight_model(cls, data: SchFlightModelData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("scheduled_flight_model", data.__dict__)

    @classmethod
    async def update_scheduled_flight_model(cls, field_id: int, data: SchFlightModelData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("scheduled_flight_model", field_id, data.__dict__)

    @classmethod
    async def delete_scheduled_flight_model(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("scheduled_flight_model", field_id)

    # AIRPLANE_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airplane_model(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.get_all_from_table("airplane_model")

    @classmethod
    async def create_airplane_model(cls, data: AirplaneModelData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("airplane_model", data.__dict__)

    @classmethod
    async def update_airplane_model(cls, field_id: int, data: AirplaneModelData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("airplane_model", field_id, data.__dict__)

    @classmethod
    async def delete_airplane_model(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("airplane_model", field_id)

    # AIRPLANE -----------------------------------------------------------------------------------------------
    @classmethod
    async def get_all_airplane(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def create_airplane(cls, data: AirplaneData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def update_airplane(cls, field_id: int, data: AirplaneData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        querydb = select(AirplaneModelModel).filter_by(name=data.airplaneModelName)
        async with new_session() as session:
            result = await session.execute(querydb)
        field = result.scalars().first()
        if field is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой модели самолёта не существует",
            )
        return await Functions.update_field("airplane", field_id,
                                            {"airplane_model_id": field.id,
                                             "registration_number": data.registrationNumber})

    @classmethod
    async def delete_airplane(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("airplane", field_id)

    # MAINTENANCE_MODEL --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_maintenance_model(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.get_all_from_table("maintenance_model")

    @classmethod
    async def create_maintenance_model(cls, data: MaintenanceModelData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("maintenance_model", data.__dict__)

    @classmethod
    async def update_maintenance_model(cls, field_id: int, data: MaintenanceModelData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("maintenance_model", field_id, data.__dict__)

    @classmethod
    async def delete_maintenance_model(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("maintenance_model", field_id)

    # JOB_TITLE --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_job_title(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.get_all_from_table("job_title")

    @classmethod
    async def create_job_title(cls, data: JobTitleData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.create_field("job_title", data.__dict__)

    @classmethod
    async def update_job_title(cls, field_id: int, data: JobTitleData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.update_field("job_title", field_id, data.__dict__)

    @classmethod
    async def delete_job_title(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("job_title", field_id)

    # EMPLOYEE --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_employee(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        querydb = select(EmployeeModel).options(joinedload(EmployeeModel.job_title))
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.scalars().all()

        data = []
        for field in fields:
            data.append({"id": field.id,
                         "jobTitleName": field.job_title.name,
                         "surname": field.surname,
                         "name": field.name,
                         "patronymic": field.patronymic,
                         "experience": field.experience})
        return data

    @classmethod
    async def create_employee(cls, data: EmployeeData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def update_employee(cls, field_id: int, data: EmployeeData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
    async def delete_employee(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("employee", field_id)

    # PRETRIP_MAINTENANCE --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_pretrip_maintenance(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
                         "datetime": field.datetime.strftime('%d-%m-%Y %H:%M'),
                         "result": field.result})
        return data

    @classmethod
    async def create_pretrip_maintenance(cls, data: PretripMaintenanceData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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

        querydb = select(AirplaneModel).filter_by(registration_number=data.registrationNumber)
        async with new_session() as session:
            result = await session.execute(querydb)
        field3 = result.scalars().first()
        if field3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого самолёта не существует",
            )
        try:
            return await Functions.create_field("pretrip_maintenance",
                                                {"maintenance_model_id": field1.id,
                                                 "employee_id": field2.id,
                                                 "airplane_id": field3.id,
                                                 "datetime": datetime.strptime(data.datetime, '%d-%m-%Y %H:%M'),
                                                 "result": data.result})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат даты",
            )

    @classmethod
    async def update_pretrip_maintenance(cls, field_id: int, data: PretripMaintenanceData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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

        querydb = select(AirplaneModel).filter_by(registration_number=data.registrationNumber)
        async with new_session() as session:
            result = await session.execute(querydb)
        field3 = result.scalars().first()
        if field3 is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такого самолёта не существует",
            )
        try:
            return await Functions.update_field("pretrip_maintenance", field_id,
                                                {"maintenance_model_id": field1.id,
                                                 "employee_id": field2.id,
                                                 "airplane_id": field3.id,
                                                 "datetime": datetime.strptime(data.datetime, '%d-%m-%Y %H:%M'),
                                                 "result": data.result})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат даты",
            )

    @classmethod
    async def delete_pretrip_maintenance(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        return await Functions.delete_field("pretrip_maintenance", field_id)

    # SCHEDULED_FLIGHT --------------------------------------------------------------------------------------
    @classmethod
    async def get_all_scheduled_flight(cls, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        querydb = select(ScheduledFlightModel).options(
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airline),
            joinedload(ScheduledFlightModel.flight)
            .joinedload(FlightModel.airport),
            joinedload(ScheduledFlightModel.airplane),
            joinedload(ScheduledFlightModel.scheduled_flight_model),
            joinedload(ScheduledFlightModel.crew)
            .joinedload(CrewModel.employee)
            .joinedload(EmployeeModel.job_title)
        )
        async with new_session() as session:
            result = await session.execute(querydb)
        fields = result.unique().scalars().all()

        data = []
        for field in fields:
            flight_data = {
                "id": field.id,
                "airlineName": field.flight.airline.name,
                "airportName": field.flight.airport.name,
                "datetimeDeparture": field.departure_datetime.strftime('%d-%m-%Y %H:%M'),
                "datetimeArrival": field.arrival_datetime.strftime('%d-%m-%Y %H:%M'),
                "registrationNumber": field.airplane.registration_number,
                "scheduledFlightModelName": field.scheduled_flight_model.name,
                "crew": []
            }
            for crew_member in field.crew:
                employee_el = crew_member.employee
                flight_data["crew"].append({
                    "employeeId": employee_el.id,
                    "name": employee_el.name,
                    "surname": employee_el.surname,
                    "patronymic": employee_el.patronymic,
                    "jobTitle": employee_el.job_title.name
                })
            data.append(flight_data)
        return data

    @classmethod
    async def create_scheduled_flight(cls, data: ScheduledFlightData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
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
        try:
            inform = await Functions.create_field("scheduled_flight",
                                                  {"flight_id": field1.id,
                                                   "airplane_id": field2.id,
                                                   "scheduled_flight_model_id": field3.id,
                                                   "departure_datetime": datetime.strptime(data.datetimeDeparture, '%d-%m-%Y %H:%M'),
                                                   "arrival_datetime": datetime.strptime(data.datetimeArrival, '%d-%m-%Y %H:%M')})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат даты",
            )

        async with new_session() as session:
            for employee_id in data.crew:
                crew_field = CrewModel(scheduled_flight_id=inform.field_id, employee_id=employee_id)
                session.add(crew_field)
            await session.commit()
        return Inform(detail="created", field_id=inform.field_id)

    @classmethod
    async def update_scheduled_flight(cls, field_id: int, data: ScheduledFlightData, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        querydb = select(FlightModel).options(
            joinedload(FlightModel.airline),
            joinedload(FlightModel.airport)
        ).join(AirlineModel).join(AirportModel).filter(
            AirlineModel.name == data.airlineName,
            AirportModel.name == data.airportName
        )
        print(data.crew)
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
        try:
            inform = await Functions.update_field("scheduled_flight", field_id,
                                                  {"flight_id": field1.id,
                                                   "airplane_id": field2.id,
                                                   "scheduled_flight_model_id": field3.id,
                                                   "departure_datetime": datetime.strptime(data.datetimeDeparture, '%d-%m-%Y %H:%M'),
                                                   "arrival_datetime": datetime.strptime(data.datetimeArrival, '%d-%m-%Y %H:%M')})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат даты",
            )

        querydb = delete(CrewModel).filter_by(scheduled_flight_id=inform.field_id)
        async with new_session() as session:
            await session.execute(querydb)
            for employee_id in data.crew:
                crew_field = CrewModel(scheduled_flight_id=inform.field_id, employee_id=employee_id)
                session.add(crew_field)
            await session.commit()
        return Inform(detail="updated", field_id=inform.field_id)

    @classmethod
    async def delete_scheduled_flight(cls, field_id: id, request: Request):
        user_info = await Functions.get_user_id_and_role(request)
        Functions.check_admin(user_info)
        querydb = delete(CrewModel).filter_by(scheduled_flight_id=field_id)
        async with new_session() as session:
            await session.execute(querydb)
            await session.commit()
        return await Functions.delete_field("scheduled_flight", field_id)
