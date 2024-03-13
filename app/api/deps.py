from fastapi import HTTPException
from fastapi.params import Depends
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.scoping import ScopedSession
from starlette import status
from starlette.requests import Request

from app.repository.user import UserRepository
from app.uow.uow import UnitOfWork
from app.service.user import UserService


def get_user_repository(requset: Request):
    sql_session_factory: ScopedSession = requset.app.state.sql_session_factory
    try:
        with UnitOfWork(sql_session_factory=sql_session_factory) as uow:
            yield uow.user_repository
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=" ".join(e.args)
        )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    yield UserService(user_repository)
