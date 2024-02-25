from typing import Callable

from sqlmodel import create_engine, Session


def create_sqlmodel_engine(url: str, **kwargs):
    return create_engine(url, **kwargs)


def create_sqlmodel_session_maker(engine) -> Callable[[], Session]:
    return lambda: Session(bind=engine, autocommit=False, autoflush=False)
