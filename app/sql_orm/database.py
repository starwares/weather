from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.orm.session import Session as SessionORM
from contextlib import contextmanager
from sqlalchemy.pool import QueuePool
from app.settings import get_settings


settings = get_settings()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope(session: SessionORM = Session) -> SessionORM:
    """Provide a transactional scope around a series of operations."""
    session = sessionmaker(bind=create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_size=20, poolclass=QueuePool, echo=True))
    sess = session()
    try:
        yield sess
        # sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.invalidate()


