from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.orm.session import Session as SessionORM
from contextlib import contextmanager
from sqlalchemy.pool import QueuePool
from app.settings import get_settings
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


settings = get_settings()

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()




