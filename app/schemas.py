from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class City(BaseModel):
    name: str
    url: str | None
    image_url: str | None
    data_lat: str
    data_lon: str


class User(BaseModel):
    id: str
    name: str
    city: Optional[City] | None

    # class Config:
    #     orm_mode = True


class Weather(BaseModel):
    id: str
    city_name: str
    degrees_Celsius: int
    day: datetime
    created: datetime

    # class Config:
    #     orm_mode = True


class Cron(BaseModel):
    id: str
    hour: int
    minutes: int
    seconds: int
    room_id: int
    city_name: str
    user_id: str

    # class Config:
    #     orm_mode = True
