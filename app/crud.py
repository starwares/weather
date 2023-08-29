import uuid

from app.sql_orm.database import session_scope
from app.sql_orm.models import City
from app.schemas import City as Pydantic_city
from typing import List


def create_user():
    pass


def update_user():
    pass


def checking_availability_user():
    with session_scope() as session:
        session.query()


def add_city_to_user():
    pass


def add_maplink_for_city(city_name: str):
    try:
        with session_scope() as session:
            city = session.query(City).filter(City.name == city_name).one()
    except Exception as e:
        print(e)
    return city.data_lat, city.data_lon


def add_city_in_db(cities: List):
    try:
        with session_scope() as session:
            city: Pydantic_city
            for city in cities:
                session.add(City(name=city.name, id=str(uuid.uuid4()), data_lat=city.data_lat, data_lon=city.data_lon))
            print("hi")
            session.commit()
    except Exception as e:
        print(e)

