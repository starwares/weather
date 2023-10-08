import uuid

from app.sql_orm.database import session as session_scope
from app.sql_orm.models import City, User, Cron
from sqlalchemy import select
from app.schemas import City as Pydantic_city
from typing import List
import asyncio


async def create_user(id: str, city_name: str, name: str = "Anonymous"):
    try:
        query_city = select(City).where(City.name == city_name)
        query_user = select(User).where(User.id == id)
        async with session_scope() as session:
            async with session.begin():
                city = await session.scalar(query_city)
                user = await session.scalar(query_user)
                if user:
                    new_user = user
                else:
                    new_user = User(id=id, name=name, city_name=city.name)
                    session.add(new_user)
                    await session.commit()
            return new_user, city
    except Exception as e:
        print(e)


async def create_cron(id_user: str, city_name: str, hour: int, minutes: int):
    user, city = await create_user(id=id_user, city_name=city_name)
    new_cron = Cron(id=str(uuid.uuid4()), hour=hour, minutes=minutes, user_id=user.id, city_name=city.name)
    async with session_scope() as session:
        async with session.begin():
            session.add(new_cron)
        await session.commit()
        return new_cron


async def delete_cron(id_user: str):
    try:
        query = select(Cron).where(Cron.user_id == id_user)
        async with session_scope() as session:
            async with session.begin():
                cron = await session.scalar(query)
                if cron:
                    await session.delete(cron)
                await session.commit()
        return cron.id
    except Exception:
        return False


async def get_cron(id_user: str):
    cron_strings = ""
    query = select(Cron).where(Cron.user_id == id_user)
    async with session_scope() as session:
        async with session.begin():
            crones = await session.scalars(query)
    if crones:
        for cron in crones:
            cron_strings += f"{cron.city_name} : {cron.hour}:{cron.minutes} \n"
        return cron_strings
    return None


async def get_all_cron():
    db_cron = []
    async with session_scope() as session:
        async with session.begin():
            statement = select(Cron)
            result = await session.execute(statement)
            db_cron = result.scalars().all()
    return db_cron


def update_user():
    pass


async def checking_availability_user():
    async with session_scope() as session:
        async with session.begin():
            session.query()


def add_city_to_user():
    pass


async def add_maplink_for_city(city_name: str):
    try:
        query = select(City).where(City.name == city_name)
        async with session_scope() as session:
            async with session.begin():
                city = await session.scalar(query)
        return city.data_lat, city.data_lon
    except Exception as e:
        print(e)


async def add_city_in_db(cities: List):
    async with session_scope() as session:
        async with session.begin():
            for city in cities:
                session.add(City(name=city.name, data_lat=city.data_lat, data_lon=city.data_lon))
        await session.commit()
    return cities


async def get_all_cities():
    db_cities = []
    async with session_scope() as session:
        async with session.begin():
            statement = select(City)
            result = await session.execute(statement)
            db_cities = result.scalars().all()
    return db_cities


async def get_city_maplink(cities: List):
    try:
        async with session_scope() as session:
            async with session.begin():
                statement = select(City)
                result = await session.execute(statement)
                db_cities = result.scalars().all()
                for db_city in db_cities:
                    for city in cities:
                        if db_city.name == city.name:
                            city.data_lat = db_city.data_lat
                            city.data_lon = db_city.data_lon
                            break
                return cities

    except Exception as e:
        print(e)


async def main():
    ar = await get_cron("750292830")
    print(ar)


if __name__ == '__main__':
    asyncio.run(main())
