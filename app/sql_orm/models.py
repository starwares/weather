from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.sql_orm.database import Base


class City(Base):
    __tablename__: str = "cities"
    name = Column(String, primary_key=True, index=True, unique=True)
    data_lat = Column(String)
    data_lon = Column(String)


class Weather(Base):
    __tablename__: str = 'weather'

    id = Column(String, primary_key=True, index=True)
    degrees_Celsius = Column(Integer, index=True)
    day = Column(DateTime, index=True)
    created = Column(DateTime, default=datetime.utcnow)

    city_name = Column(String, ForeignKey('cities.name'))
    city = relationship("City", backref="weather")


class User(Base):
    __tablename__: str = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

    city_name = Column(String, ForeignKey('cities.name'))
    cities = relationship("City", backref="users")


class Cron(Base):
    __tablename__: str = "crons"

    id = Column(String, primary_key=True, index=True)
    hour = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer)
    room_id = Column(String)
    user_id = Column(String, ForeignKey('users.id'))
    user = relationship("User", backref="crons")
    city_name = Column(String, ForeignKey('cities.name'))
    cities = relationship("City", backref="crons")

