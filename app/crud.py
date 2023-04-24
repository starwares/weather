import uuid

from app.sql_orm.database import session_scope, get_db
from app.sql_orm.models import City
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


def add_city_in_db(cities: List):
    cities = set(cities)
    try:
        with session_scope() as session:
            for city in cities:
                session.add(City(name=city, id=str(uuid.uuid4())))
            session.commit()
    except Exception as e:
        print(e)

