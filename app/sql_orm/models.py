from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.sql_orm.database import Base


class City(Base):
    __tablename__: str = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)


class Weather(Base):
    __tablename__: str = 'weather'

    id = Column(Integer, primary_key=True, index=True)
    degrees_Celsius = Column(Integer, index=True)
    day = Column(DateTime, index=True)
    created = Column(DateTime, default=datetime.utcnow)

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship("City", backref="weather", cascade="all, delete-orphan")


class User(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    city_id = Column(Integer, ForeignKey('cities.id'))
    cities = relationship("City", backref="users")


class Cron(Base):
    __tablename__: str = "crons"

    id = Column(Integer, primary_key=True, index=True)
    hour = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer)
    room_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="crons")
    city_id = Column(Integer, ForeignKey('cities.id'))
    cities = relationship("City", backref="crons")

