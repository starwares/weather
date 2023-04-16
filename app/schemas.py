from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    name: str
    city: Optional[City] | None


class Weather(BaseModel):
    id: int
    city_id: int
    degrees_Celsius: int
    day: datetime
    created: datetime

    class Config:
        orm_mode = True


class Cron(BaseModel):
    id: int
    hour: int
    minutes: int
    seconds: int
    room_id: int
    city_id: int
    user_id: int

    class Config:
        orm_mode = True
