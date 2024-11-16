from typing import Any
import sqlite3
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from datetime import datetime

engine = create_async_engine("sqlite+aiosqlite:///./site.db", connect_args={})
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class CountryModel(Model):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country_geocode: Mapped[str] = mapped_column(String(3))


class SettlementModel(Model):
    __tablename__ = "settlement"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(50))


class AirportModel(Model):
    __tablename__ = "airport"

    id: Mapped[int] = mapped_column(primary_key=True)
    settlement_id: Mapped[int] = mapped_column(ForeignKey("settlement.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    adress: Mapped[str] = mapped_column(String(256))

    flight: Mapped[list["FlightModel"]] = relationship()


class AirlineModel(Model):
    __tablename__ = "airline"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class FlightModel(Model):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    airline_id: Mapped[int] = mapped_column(ForeignKey("airline.id", ondelete="CASCADE"))
    airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id", ondelete="CASCADE"))


class AirplaneModelModel(Model):
    __tablename__ = "airplane_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[float]


class AirplaneModel(Model):
    __tablename__ = "airplane"

    id: Mapped[int] = mapped_column(primary_key=True)
    airplane_model_id: Mapped[int] = mapped_column(ForeignKey("airplane_model.id", ondelete="CASCADE"))
    registration_number: Mapped[str] = mapped_column(String(100))


class JobTitleModel(Model):
    __tablename__ = "job_title"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class EmployeeModel(Model):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_title_id: Mapped[int] = mapped_column(ForeignKey("job_title.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str] = mapped_column(String(100))
    experience: Mapped[str] = mapped_column(String(50))


class CrewModel(Model):
    __tablename__ = "crew"

    flight_id: Mapped[int] = mapped_column(ForeignKey("scheduled_flight.id", ondelete="CASCADE"), primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"), primary_key=True)


class ScheduledFlightModelModel(Model):
    __tablename__ = "scheduled_flight_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class ScheduledFlightModel(Model):
    __tablename__ = "scheduled_flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flight.id", ondelete="CASCADE"))
    scheduled_flight_model_id: Mapped[int] = mapped_column(ForeignKey("scheduled_flight_model.id", ondelete="CASCADE"))
    airplane_id: Mapped[int] = mapped_column(ForeignKey("airplane.id", ondelete="CASCADE"))
    departure_datetime: Mapped[datetime]
    arrival_datetime: Mapped[datetime]

    crew: Mapped[list["CrewModel"]] = relationship()


class UserModel(Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))

    flight_history: Mapped[list["FlightHistoryModel"]] = relationship()


class FlightHistoryModel(Model):
    __tablename__ = "flight_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    scheduled_flight_id: Mapped[int] = mapped_column(ForeignKey("scheduled_flight.id", ondelete="CASCADE"))
    payment_datetime: Mapped[datetime]
    seat: Mapped[str] = mapped_column(String(10))


class MaintenanceModelModel(Model):
    __tablename__ = "maintenance_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))


class PretripMaintenanceModel(Model):
    __tablename__ = "pretrip_maintenance"

    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_model_id: Mapped[int] = mapped_column(ForeignKey("maintenance_model.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"))
    airplane_id: Mapped[int] = mapped_column(ForeignKey("airplane.id", ondelete="CASCADE"))
    datetime: Mapped[datetime]
    result: Mapped[str] = mapped_column(String(100))


class ShopModel(Model):
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(256))


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    conn = sqlite3.connect('site.db')
    conn.execute("PRAGMA foreign_keys = TRUE;")
    conn.close()

