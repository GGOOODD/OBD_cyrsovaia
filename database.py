from typing import Any
import sqlite3
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, event
from datetime import datetime

from sqlalchemy.engine import Engine


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = create_async_engine("sqlite+aiosqlite:///./site.db", connect_args={})
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class CountryModel(Model):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    geocode: Mapped[str] = mapped_column(String(3))


class SettlementModel(Model):
    __tablename__ = "settlement"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(50))

    country: Mapped["CountryModel"] = relationship()


class AirportModel(Model):
    __tablename__ = "airport"

    id: Mapped[int] = mapped_column(primary_key=True)
    settlement_id: Mapped[int] = mapped_column(ForeignKey("settlement.id"))
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(256))

    settlement: Mapped["SettlementModel"] = relationship()


class AirlineModel(Model):
    __tablename__ = "airline"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class FlightModel(Model):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    airline_id: Mapped[int] = mapped_column(ForeignKey("airline.id"))
    airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))

    airport: Mapped["AirportModel"] = relationship()
    airline: Mapped["AirlineModel"] = relationship()


class AirplaneModelModel(Model):
    __tablename__ = "airplane_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[float]


class AirplaneModel(Model):
    __tablename__ = "airplane"

    id: Mapped[int] = mapped_column(primary_key=True)
    airplane_model_id: Mapped[int] = mapped_column(ForeignKey("airplane_model.id"))
    registration_number: Mapped[str] = mapped_column(String(100))

    airplane_model: Mapped["AirplaneModelModel"] = relationship()


class JobTitleModel(Model):
    __tablename__ = "job_title"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class EmployeeModel(Model):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_title_id: Mapped[int] = mapped_column(ForeignKey("job_title.id"))
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str] = mapped_column(String(100))
    experience: Mapped[str] = mapped_column(String(50))

    job_title: Mapped["JobTitleModel"] = relationship()


class CrewModel(Model):
    __tablename__ = "crew"

    scheduled_flight_id: Mapped[int] = mapped_column(ForeignKey("scheduled_flight.id"), primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), primary_key=True)

    employee: Mapped["EmployeeModel"] = relationship()


class ScheduledFlightModelModel(Model):
    __tablename__ = "scheduled_flight_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class ScheduledFlightModel(Model):
    __tablename__ = "scheduled_flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flight.id"))
    scheduled_flight_model_id: Mapped[int] = mapped_column(ForeignKey("scheduled_flight_model.id"))
    airplane_id: Mapped[int] = mapped_column(ForeignKey("airplane.id"))
    departure_datetime: Mapped[datetime]
    arrival_datetime: Mapped[datetime]

    flight: Mapped["FlightModel"] = relationship()
    scheduled_flight_model: Mapped["ScheduledFlightModelModel"] = relationship()
    airplane: Mapped["AirplaneModel"] = relationship()
    crew: Mapped[list["CrewModel"]] = relationship(uselist=True)


class UserModel(Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    admin: Mapped[bool]


class FlightHistoryModel(Model):
    __tablename__ = "flight_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    scheduled_flight_id: Mapped[int] = mapped_column(ForeignKey("scheduled_flight.id"))
    payment_datetime: Mapped[datetime]
    seat: Mapped[str] = mapped_column(String(10))

    scheduled_flight: Mapped["ScheduledFlightModel"] = relationship()


class MaintenanceModelModel(Model):
    __tablename__ = "maintenance_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))


class PretripMaintenanceModel(Model):
    __tablename__ = "pretrip_maintenance"

    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_model_id: Mapped[int] = mapped_column(ForeignKey("maintenance_model.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    airplane_id: Mapped[int] = mapped_column(ForeignKey("airplane.id"))
    datetime: Mapped[datetime]
    result: Mapped[str] = mapped_column(String(100))

    maintenance_model: Mapped["MaintenanceModelModel"] = relationship()
    employee: Mapped["EmployeeModel"] = relationship()
    airplane: Mapped["AirplaneModel"] = relationship()


class ShopModel(Model):
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(256))


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    # conn = sqlite3.connect('site.db')
    # conn.execute("PRAGMA foreign_keys = ON;")
    # conn.close()

